"""
Name: module_page_manager.py
definition: a script to generate and delete annotation term page
Contributors: Dan Lu, Nicholas Lee
"""

# load modules
import glob
import os
import re
from functools import partial
import frontmatter
import numpy as np
import pandas as pd
from mdutils import fileutils
from dotenv import dotenv_values

config = dotenv_values(".env")


def get_info(data_model, term, column="Attribute"):
    """
    Function to get a dictionary for term definition, definition source, module

    :param term: the term name

    :returns: a dictionary with keys: Description and module
    """
    # get the definition and module of the term from data model
    results = data_model.loc[
        data_model[column] == term, ["Description", "Source", "Module"]
    ].to_dict("records")

    return results


def create_template_page(term, term_dict):
    # load template for templates in data model
    post = frontmatter.load("_layouts/template_page_template.md")
    post.metadata["title"] = re.sub("([A-Z]+)|_", r" \1", term).strip()
    post.metadata["parent"] = term_dict["Module"]
    post.content = (
        "{% assign mydata=site.data."
        + re.sub("\s|/", "_", term)
        + " %} \n{: .note-title } \n"
        + f">{post.metadata['title']}\n"
        + ">\n"
        + f">{term_dict['Description']} [[Source]]({term_dict['Source']})\n"
        + post.content
    )

    # create file
    file = fileutils.MarkDownFile(f"docs/{term_dict['Module']}/{term}")

    # add content to the file
    file.append_end(frontmatter.dumps(post))

    return post


def create_table_page(term, term_dict):
    # load markdown template for a page on the website
    post = frontmatter.load("_layouts/term_page_template.md")
    post.metadata["title"] = term
    post.content = (
        "{% assign mydata=site.data."
        + term
        + " %} \n{: .note-title } \n"
        + f">{term}\n"
        + ">\n"
        + f">{term_dict['Description']} [[Source]]({term_dict['Source']})\n"
        + post.content
    )
    post.metadata["parent"] = term_dict["Module"]

    return post


def create_module_page(module):
    # load markdown template for a page on the website
    post = frontmatter.load("_layouts/term_page_template.md")
    post.metadata["title"] = module
    post.metadata["nav_order"] = 5
    post.metadata["permalink"] = f"docs/Modules/{module}.html"
    post.metadata["parent"] = "Modules"
    post.content = (
        "{% assign mydata=site.data."
        + re.sub("\s|/", "_", module)
        + " %} \n{: .note-title } \n"
        + f">{module}\n"
        + ">\n"
        + ">Module in the data modele\n"
        + post.content
    )

    # create a module page
    module_page = fileutils.MarkDownFile(f"docs/Modules/{module}")

    # add content to the file
    module_page.append_end(frontmatter.dumps(post))

    return module_page


def create_full_table(data_model):
    # name of the data model to use
    module_name = "DataModel"

    # Create CSV for table
    df = data_model.rename(
        {"Attribute": "Key", "Description": "Key Description"}, axis=1, errors="ignore"
    )
    df = df[["Key", "Key Description", "Type", "Source", "Module"]]
    df.to_csv(f"_data/{module_name}.csv", index=False)

    # create directory for the moduel if not exist
    if not os.path.exists(f"docs/{module_name}/"):
        os.mkdir(f"docs/{module_name}/")

    # create a module page
    module = fileutils.MarkDownFile(f"docs/{module_name}/{module_name}")

    # creating markdown text
    post = frontmatter.load("_layouts/term_page_template.md")
    del post.metadata["parent"]
    post.metadata["title"] = module_name
    post.metadata["nav_order"] = 2
    post.metadata["permalink"] = f"docs/{module_name}.html"

    post.content = (
        "{% assign mydata=site.data."
        + module_name
        + " %} \n{: .note-title } \n"
        + f">{module_name}\n"
        + ">\n"
        + f">Complete Table of Keys for ELITE that are found in the data model\n"
        + post.content
    )

    # add table to module page
    module.append_end(frontmatter.dumps(post))


def delete_page(term):
    """Delete unneeded terms

    :param term: attribute found in the data model
    :type term: str
    """
    for file in glob.glob("docs/*/*.md"):
        if file.split("/")[-1].split(".")[0] == term:
            os.remove(file)


if __name__ == "__main__":
    # load data model csv file
    data_model = pd.read_csv(config["csv_model"])
    data_model.fillna("", inplace=True)

    # generate a full table in case there needs to be some references to it
    create_full_table(data_model)

    # generate module pages
    modules = data_model["Module"].unique().tolist()
    for m in modules:
        module_page = create_module_page(m)

    # generate pages for templates
    templates = (
        data_model.loc[data_model["Parent"] == "Template", "Attribute"]
        .unique()
        .tolist()
    )

    for t in templates:
        # quick cleanup
        term_attr = re.sub("_", " ", t)

        # get term information
        results = get_info(data_model, term_attr, column="Attribute")[0]

        template_page = create_template_page(t, term_dict=results)

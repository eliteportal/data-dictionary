"""
Name: term_page_manager.py
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


def get_term_info(data_model, term):
    """
    Function to get a dictionary for term definition, definition source, module

    :param term: the term name

    :returns: a dictionary with keys: Description and module
    """
    # get the definition and module of the term from data model
    results = data_model.loc[
        data_model["Attribute"] == term, ["Description", "Source", "Module"]
    ].to_dict("records")

    return results


def create_template_page(term, term_dict):
    # load template for templates in data model
    post = frontmatter.load("template_page_template.md")
    post.metadata["title"] = re.sub("([A-Z]+)|_", r" \1", term).title()
    post.metadata["permalink"] = f'docs/{post.metadata["title"]}.html'
    post.content = (
        "{% assign mydata=site.data."
        + term
        + " %} \n{: .note-title } \n"
        + f">{post.metadata['title']}\n"
        + ">\n"
        + f">{term_dict['Description']} [[Source]]({term_dict['Source']})\n"
        + post.content
    )
    return post


def create_table_page(term, term_dict):
    # load markdown template for a page on the website
    post = frontmatter.load("term_page_template.md")
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


def create_module_page(module, term_dict):
    # load template for templates in data model
    post = frontmatter.load("template_page_template.md")
    post.metadata["title"] = re.sub("([A-Z]+)|_", r" \1", module).title()
    post.metadata["permalink"] = f'docs/{post.metadata["title"]}.html'
    post.content = (
        "{% assign mydata=site.data."
        + module
        + " %} \n{: .note-title } \n"
        + f">{post.metadata['title']}\n"
        + ">\n"
        + f">{term_dict['Description']} [[Source]]({term_dict['Source']})\n"
        + post.content
    )
    return post


def generate_page(data_model, term):
    """
    Function to generate term/template markdown page

    :param term: the term name

    :returns: a term Markdown page generated under the docs/<module_name> folder
    """
    # quick cleanup
    term_attr = re.sub("_", " ", term)

    # get term information
    results = get_term_info(data_model, term_attr)[0]

    # Try to add source
    for i in results:
        try:
            if results[i]["Source"] == "Sage Bionetworks":
                results[i]["Source"] = "https://sagebionetworks.org/"
        except IndexError:
            results[i]["Source"] = ""

    if "Template" in data_model.query("Attribute == @term")["Module"].values:
        post = create_template_page(term, term_dict=results)

    else:
        post = create_table_page(term, term_dict=results)

    # create directory for the moduel if not exist
    if not os.path.exists(f"docs/{results['Module']}/"):
        os.mkdir(f"docs/{results['Module']}/")

        # create a module page
        module = fileutils.MarkDownFile(f"docs/{results['Module']}/{results['Module']}")

        if "Template" in data_model.query("Attribute == @term")["Module"].values:
            # add permalink for template page
            module.append_end(
                f"--- \nlayout: page \ntitle: {results['Module']} \nhas_children: true \nnav_order: 5 \npermalink: docs/{results['Module']}.html \n---"
            )
        else:
            module.append_end(
                f"--- \nlayout: page \ntitle: {results['Module']} \nhas_children: true \nnav_order: 2 \npermalink: docs/{results['Module']}.html \n---"
            )

    # create file
    file = fileutils.MarkDownFile(f"docs/{results['Module']}/{term}")

    # add content to the file
    file.append_end(frontmatter.dumps(post))


def generate_full_table(data_model):
    # name of the data model to use
    site_data = "dataModel"
    module_name = "FullTable"

    # Creating markdown file for module
    # create directory for the moduel if not exist
    if not os.path.exists(f"docs/{module_name}/"):
        os.mkdir(f"docs/{module_name}/")

    # create a module page
    module = fileutils.MarkDownFile(f"docs/{module_name}/{module_name}")

    module.append_end(
        f"--- \nlayout: page \ntitle: {module_name} \nhas_children: true \nnav_order: 2 \npermalink: docs/{module_name}.html \n---"
    )

    # Create CSV for table
    data_model = data_model.rename(
        {"Attribute": "Key", "Description": "Key Description"}, axis=1
    )
    data_model = data_model[["Key", "Key Description", "Type", "Source", "Module"]]
    data_model.to_csv(f"_data/{site_data}.csv", index=False)

    # creating markdown text
    post = frontmatter.load("term_page_template.md")
    post.metadata["title"] = site_data
    post.content = (
        "{% assign mydata=site.data."
        + site_data
        + " %} \n{: .note-title } \n"
        + f">{site_data}\n"
        + ">\n"
        + f">Full Table of Keys for ELITE\n"
        + post.content
    )
    post.metadata["parent"] = module_name

    # create file
    file = fileutils.MarkDownFile(f"docs/{module_name}/{site_data}")
    # add content to the file
    file.append_end(frontmatter.dumps(post))


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

    # pull terms
    term_files = [
        file.split("/")[-1].split(".")[0] for file in glob.glob("_data/*.csv")
    ]

    term_pages = [
        file.split("/")[-1].split(".")[0] for file in glob.glob("docs/**/*.md")
    ]

    to_add = map(str, np.setdiff1d(term_files, term_pages))

    # generate pages for terms with the term files
    generate_page_temp = partial(generate_page, data_model)
    list(map(generate_page_temp, to_add))

    # delete pages for terms without the term files and exclude module and template pages (since template page might be named differently from the template files)
    to_delete = np.setdiff1d(term_pages, term_files)
    to_delete = np.setdiff1d(set(to_delete), set(["FullTable", "Template"])).tolist()
    print(f"Deleting: {to_delete}")

    to_delete = [
        x
        for x in to_delete
        if x not in data_model["Module"].dropna().unique().tolist()
        and "Template" not in x
    ]

    list(map(delete_page, to_delete))

    generate_full_table(data_model)

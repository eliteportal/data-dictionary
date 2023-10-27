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

import yaml

with open("./_config.yml", "r") as f:
    config = yaml.safe_load(f)


def get_term_info(data_model, term):
    """
    Function to get a dictionary for term definition, definition source, module

    :param term: the term name

    :returns: a dictionary with keys: Description and module
    """
    # get the definition and module of the term from data model
    results = data_model.loc[
        data_model["Attribute"] == term, ["Description", "Source", "module"]
    ].to_dict("records")

    return results


def generate_page(data_model, term):
    """
    Function to generate term/template markdown page

    :param term: the term name

    :returns: a term Markdown page generated under the docs/<module_name> folder
    """
    term_attr = re.sub("_", " ", term)

    # get term information
    results = get_term_info(data_model, term_attr)

    # add paragraph for term definition and source
    try:
        if results[0]["Source"] == "Sage Bionetworks":
            results[0]["Source"] = "https://sagebionetworks.org/"
    except IndexError:
        results[0]["Source"] = ""

    if "Template" in data_model.query("Attribute == @term")["module"].values:
        # load template
        post = frontmatter.load("template_page_template.md")
        post.metadata["title"] = re.sub("([A-Z]+)|_", r" \1", term).title()
        post.metadata["permalink"] = f'docs/{post.metadata["title"]}.html'
        post.content = (
            "{% assign mydata=site.data."
            + term
            + " %} \n{: .note-title } \n"
            + f">{post.metadata['title']}\n"
            + ">\n"
            + f">{results[0]['Description']} [[Source]]({results[0]['Source']})\n"
            + post.content
        )
    else:
        # load template
        post = frontmatter.load("term_page_template.md")
        post.metadata["title"] = term
        post.content = (
            "{% assign mydata=site.data."
            + term
            + " %} \n{: .note-title } \n"
            + f">{term_attr}\n"
            + ">\n"
            + f">{results[0]['Description']} [[Source]]({results[0]['Source']})\n"
            + post.content
        )
    post.metadata["parent"] = results[0]["module"]

    # create directory for the moduel if not exist
    if not os.path.exists(f"docs/{results[0]['module']}/"):
        os.mkdir(f"docs/{results[0]['module']}/")

        # create a module page
        module = fileutils.MarkDownFile(
            f"docs/{results[0]['module']}/{results[0]['module']}"
        )

        if "Template" in data_model.query("Attribute == @term")["module"].values:
            # add permalink for template page
            module.append_end(
                f"--- \nlayout: page \ntitle: {results[0]['module']} \nhas_children: true \nnav_order: 5 \npermalink: docs/{results[0]['module']}.html \n---"
            )
        else:
            module.append_end(
                f"--- \nlayout: page \ntitle: {results[0]['module']} \nhas_children: true \nnav_order: 2 \npermalink: docs/{results[0]['module']}.html \n---"
            )

    # create file
    file = fileutils.MarkDownFile(f"docs/{results[0]['module']}/{term}")

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
    data_model = data_model[["Key", "Key Description", "Type", "Source", "module"]]
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
    for file in glob.glob("docs/*/*.md"):
        if file.split("/")[-1].split(".")[0] == term:
            os.remove(file)


def main():
    # load data model csv file
    data_model = pd.read_csv(config["data_model"])

    data_model.fillna("", inplace=True)

    # pull terms
    term_files = [
        file.split("/")[-1].split(".")[0] for file in glob.glob("_data/*.csv")
    ]

    term_pages = [
        file.split("/")[-1].split(".")[0] for file in glob.glob("docs/*/*.md")
    ]

    to_add = map(str, np.setdiff1d(term_files, term_pages))

    to_delete = np.setdiff1d(term_pages, term_files).tolist()

    # pdb.set_trace()
    # generate pages for terms with the term files

    generate_page_temp = partial(generate_page, data_model)

    list(map(generate_page_temp, to_add))

    # delete pages for terms without the term files and exclude module and template pages (since template page might be named differently from the template files)
    to_delete = [
        x
        for x in to_delete
        if x not in data_model["module"].dropna().unique().tolist()
        and "Template" not in x
    ]

    list(map(delete_page, to_delete))

    generate_full_table(data_model)


if __name__ == "__main__":
    main()

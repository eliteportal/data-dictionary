"""
Name: term_page_manager.py
definition: a script to generate and delete annotation term page
Contributors: Dan Lu
"""
# load modules
import argparse
import glob
import os
import pdb
import re
import string
from functools import partial

import frontmatter
import numpy as np
import pandas as pd
from mdutils import fileutils


def get_term_info(data_model,term):
    """
    Function to get a dictionary for term definition, definition source, module

    :param term: the term name

    :returns: a dictionary with keys: Description and Module
    """
    # get the definition and module of the term from data model
    results = data_model.loc[
        data_model["Attribute"] == term, ["Description", "Source", "Module"]
    ].to_dict("records")
    return results


def generate_page(data_model, term):
    """
    Function to generate term/template markdown page

    :param term: the term name

    :returns: a term Markdown page generated under the docs/<module_name> folder
    """
    # get term information
    results = get_term_info(data_model, term)
    # add paragraph for term definition and source
    if results[0]["Source"] == "Sage Bionetworks":
        results[0]["Source"] = "https://sagebionetworks.org/"
    if 'Template' in term:
        # load template
        post = frontmatter.load("template_page_template.md")
        post.metadata["title"] = re.sub('([A-Z]+)', r' \1', term).title()
        post.metadata['permalink'] = f'docs/{post.metadata["title"]}.html'
    else:    
        # load template
        post = frontmatter.load("term_page_template.md")
        post.metadata["title"] = term
    post.metadata["parent"] = results[0]["Module"]

    # load input data and term/template description
    if 'Template' in term:
        post.content = (
        "{% assign mydata=site.data."
        + f"{term}"
        + " %} \n{: .note-title } \n"
        + f">{post.metadata['title']}\n"
        + ">\n"
        + f">{results[0]['Description']} [[Source]]({results[0]['Source']})\n"
        + post.content
    )
    else: 
        post.content = (
            "{% assign mydata=site.data."
            + f"{term}"
            + " %} \n{: .note-title } \n"
            + f">{term}\n"
            + ">\n"
            + f">{results[0]['Description']} [[Source]]({results[0]['Source']})\n"
            + post.content
        )
        
    # create directory for the moduel if not exist
    if not os.path.exists(f"docs/{results[0]['Module']}/"):
        os.mkdir(f"docs/{results[0]['Module']}/")
        # create a module page
        module = fileutils.MarkDownFile(f"docs/{results[0]['Module']}/{results[0]['Module']}")
        if 'Template' in term:
            # add permalink for template page
            module.append_end(f"--- \nlayout: page \ntitle: {results[0]['Module']} \nhas_children: true \nnav_order: 5 \npermalink: docs/{results[0]['Module']}.html \n---")
        else: 
            module.append_end(f"--- \nlayout: page \ntitle: {results[0]['Module']} \nhas_children: true \nnav_order: 2 \npermalink: docs/{results[0]['Module']}.html \n---")
    
    # create file
    file = fileutils.MarkDownFile(f"docs/{results[0]['Module']}/{term}")
    # add content to the file
    file.append_end(frontmatter.dumps(post))

def delete_page(term):
    for file in glob.glob("docs/*/*.md"):
        if file.split('/')[-1].split('.')[0] == term:
            os.remove(file)
def main():
    # load data model csv file
    data_model = pd.read_csv("veoibd.data.model.csv")
    # pull terms 
    term_files = [file.split('/')[-1].split('.')[0] for file in glob.glob("_data/*.csv")]
    term_pages = [file.split('/')[-1].split('.')[0] for file in glob.glob("docs/*/*.md")]
    to_add = map(str,np.setdiff1d(term_files,term_pages))
    to_delete = np.setdiff1d(term_pages,term_files).tolist()
    #pdb.set_trace()
    # generate pages for terms with the term files
    generate_page_temp = partial(generate_page, data_model)
    list(map(generate_page_temp, to_add))
    # delete pages for terms without the term files and exclude module and template pages (since template page might be named differently from the template files)
    to_delete = [x for x in to_delete if x not in data_model['Module'].dropna().unique().tolist() and 'Template' not in x ]
    list(map(delete_page, to_delete))

if __name__ == "__main__":
    main()


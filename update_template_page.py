"""
Name: update_template_page.py
definition: a script to update template page when new term page is created
Contributors: Dan Lu
"""
# load modules
import os
import pdb

import pandas as pd


def get_terms():
    """
    Function to extract terms with markdown page, excluding module and template pages
    """
    terms = [
        filename.split(".md")[0]
        for dirpath, _, filenames in os.walk("docs/")
        for filename in filenames
        if (
            filename.endswith(".md")
            and filename.split(".md")[0] not in os.listdir("docs")
        )
        and not "Template" in filename.split(".md")[0]
    ]
    return terms


def update_markdown(file_name, terms):
    # Load the file into file_content
    file_content = [line for line in open(f"docs/Metadata Templates/{file_name}")]
    with open(f"docs/Metadata Templates/{file_name}", "w") as writer:
        for line in file_content:
            # We search for the correct section
            if line.startswith("  var pages"):
                line = f"  var pages = {terms}\n"

            # Re-write the file at each iteration
            writer.write(line)


def main():
    # get the template pages
    templates = [
        file
        for file in os.listdir("docs/Metadata Templates/")
        if (file.endswith(".md")) & (file != "Metadata Templates.md")
    ]
    # get the terms with markdown page
    terms = get_terms()
    [update_markdown(template, terms) for template in templates]


if __name__ == "__main__":
    main()

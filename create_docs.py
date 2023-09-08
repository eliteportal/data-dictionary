"""
Name: create_docs.py
definition: A script to create the csvs that populate the metadata dictionary website
Contributors: Nicholas Lee
"""

# import packages
import os
import yaml
import pandas as pd

import term_file_manager as tfm
import term_page_manager as tpm
import update_template_page as utp

with open("./_config.yml", "r") as f:
    config = yaml.safe_load(f)


def create_module_csv(data_model, module):
    # filter data model for modules

    OUTPUT_PATH_BASE = "_data"

    data_model.query(f'Module == "{module}"').to_csv(
        os.path.join(OUTPUT_PATH_BASE, module + ".csv")
    )


def main():
    # data_model = pd.read_csv(config["data_model"])

    # data_model = data_model[["Attribute", "Description", "Type", "Source", "Module"]]

    # # rename columns
    # data_model = data_model.rename(
    #     {"Attribute": "Key", "Description": "Key Description"}
    # )

    # # Create Module CSVs
    # modules = data_model["Module"].dropna().unique()

    # for m in modules:
    #     create_module_csv(data_model, m)

module_header = """
---
layout: page
title: template
datatable: true
parent: module
permalink: permalink
---
"""

from jinja2 import Template
import codecs

#create an dict will all data that will be populate the template

def create_module_dict(module): 
    module = {}
    module.name = 'training-kit'
    module.url = 'https://github.com/github/training-kit'
    module.branches = [
        ['master',15],
        ['dev',2]
    ]
    
    return module

#render the template page
with open('term_doc_template.md', 'r') as file:
  template = Template(file.read(),trim_blocks=True)

rendered_file = template.render(module=module)

#output the file
output_file = codecs.open(f"{module}.md", "w", "utf-8")
output_file.write(rendered_file)
output_file.close()


# if __name__ == "__main__":
#     main()

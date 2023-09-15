# import packages
import os
import yaml
import pandas as pd

import term_file_manager as tfm
import term_page_manager as tpm
import update_template_page as utp

with open("./_config.yml", "r") as f:
    config = yaml.safe_load(f)


def get_subdirectories(directory):
    subdirectories = []

    for item in os.listdir(directory):
        if os.path.isdir(item):
            subdirectories.append(item)

    return subdirectories

data_model = pd.read_csv("EL.data.model.csv")

OUTPUT_PATH_BASE = "_data"

subdirectories = os.listdir("./docs")

module_list = data_model["Module"].unique().tolist()

print(subdirectories)

print(module_list)

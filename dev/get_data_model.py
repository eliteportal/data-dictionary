#! bin/bash python3
"""
Name: get_data_model.py
definition: Update data model in this directory with the data model from the data-model repo
Contributors: Nicholas Lee

Notes: 
- NA
"""

# update EL model in repo with data-models version
from utils import utils
import pathlib
from dotenv import dotenv_values


def main():
    config = dotenv_values(".env")
    url = config["csv_model"]
    try:
        df = utils.load_and_backup_dm(url, pathlib.Path("./backups").resolve())
        df.to_csv(pathlib.Path("./EL.data.model.csv").resolve(), index=False)
        print(pathlib.Path("./EL.data.model.csv").resolve())
        print("\033[92m Successfully updated data model \033[00m")
    except Exception as e:
        print("\033[31m Unable to update data model \033[00m")
        print(e)


if __name__ == "__main__":
    main()

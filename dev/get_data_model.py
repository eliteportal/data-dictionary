"""
Name: get_data_model.py
definition: Update data model in this directory with the data model from the data-model repo
Contributors: Nicholas Lee

Notes: 
- NA
"""

# update EL model in repo with data-models version
import utils
import pathlib


def main():
    url = "https://raw.githubusercontent.com/eliteportal/data-models/dev/EL.data.model.csv"
    df = utils.utils.load_and_backup_dm(url, "../backups")
    df.to_csv(pathlib.Path("../EL.data.model.csv").resolve())
    print("Successfully updated data model")


if __name__ == "main":
    main()

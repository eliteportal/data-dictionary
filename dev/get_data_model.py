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


def main():
    url = "https://raw.githubusercontent.com/eliteportal/data-models/dev/EL.data.model.csv"
    df = utils.load_and_backup_dm(url, pathlib.Path("./backups").resolve())
    df.to_csv(pathlib.Path("./EL.data.model.csv").resolve(), index=False)
    print(pathlib.Path("./EL.data.model.csv").resolve())
    print("Successfully updated data model")


if __name__ == "__main__":
    main()

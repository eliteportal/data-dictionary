"""
Name: term_file_manager.py
definition: a script to generate/update term csv 
parameters: term (str): the term name (optional)
Contributors: Dan Lu, Nicholas Lee

Notes: 
- CSV names cannot have spaces
"""
# load modules
import argparse
import os

# import pdb
from functools import partial
import re

import pandas as pd

import yaml

with open("./_config.yml", "r") as f:
    config = yaml.safe_load(f)


def get_template_keys(data_model, template):
    # extrace dependsOn values for the tempalte
    depends_on = (
        data_model.loc[data_model["Attribute"] == template, "DependsOn"]
        .str.split(",")
        .values[0]
    )

    # extract dependencies for valid values of required attributes
    valid_values = (
        data_model.loc[data_model["Attribute"].isin(depends_on), "Valid Values"]
        .dropna()
        .tolist()
    )

    valid_values = list(
        set([value for values_list in valid_values for value in values_list.split(",")])
    )

    # get the dependsOn values for valid values and concatenate it with original dependsOn list of the template
    depend_on_ext = (
        data_model.loc[data_model["Attribute"].isin(valid_values), "DependsOn"]
        .dropna()
        .tolist()
    )

    depend_on_ext = list(
        set(
            [value for values_list in depend_on_ext for value in values_list.split(",")]
        )
    )

    depends_on.extend(depend_on_ext)

    return depends_on


def create_term_df(data_model, term):
    if "Template" in data_model.query("Attribute == @term")["Module"].values:
        # generate csv for template
        depends_on = get_template_keys(data_model, term)

        # filter out attributes from data model table
        df = data_model.loc[data_model["Attribute"].isin(depends_on),]

        # # filter out valid values from data model table. DM uses Parent to distinguish types of attributes
        # df = df.loc[df["Parent"] != "validValue",]

        df = df[
            [
                "Attribute",
                "Description",
                "Type",
                "Valid Values",
                "DependsOn",
                "Required",
                "Source",
                "Module",
            ]
        ].reset_index(drop=True)

        df.rename(
            columns={"Attribute": "Key", "Description": "Key Description"}, inplace=True
        )
    else:
        prohibit = ["validValue", "BaseAnnotation", "Other"]

        df = data_model.loc[~data_model["Parent"].isin(prohibit),]

        df = df.loc[
            (df["Attribute"] == term) & (data_model["Parent"] != "validValue"),
        ][["Attribute", "Valid Values", "DependsOn", "Type", "Module"]]

        # generate csv for term
        df = (
            df.drop(columns=["Attribute", "DependsOn"])
            .set_index(["Type", "Module"])
            .apply(lambda x: x.str.split(",").explode())
            .reset_index()
        )

        # add columns
        df.rename(columns={"Valid Values": "Key"}, inplace=True)
        df = df.assign(**dict([(_, None) for _ in ["Key Description", "Source"]]))
        df = df[["Key", "Key Description", "Type", "Source", "Module"]]

    return df


def generate_csv(data_model, term):
    """_summary_

    Args:
        data_model (_type_): _description_
        term (_type_): _description_
    """

    df = create_term_df(data_model, term)

    term_csv_name = re.sub("\s|/", "_", term)

    # print(term_csv_name)

    # write out data frame
    df.to_csv(os.path.join("./_data", re.sub("\s|/", "_", term) + ".csv"), index=False)
    print("\033[92m {} \033[00m".format(f"Added {term_csv_name}.csv"))


def update_csv(data_model, term):
    """_summary_

    Args:
        data_model (_type_): _description_
        term (_type_): _description_
    """
    term_csv_name = re.sub("\s|/", "_", term)

    if "Template" in data_model.query("Attribute == @term")["Module"].values:
        depends_on = get_template_keys(data_model, term)
        new = data_model.loc[data_model["Attribute"].isin(depends_on),]
        new = new[
            [
                "Attribute",
                "Description",
                "Type",
                "Valid Values",
                "DependsOn",
                "Required",
                "Source",
                "Module",
            ]
        ].reset_index(drop=True)
        new.rename(
            columns={"Attribute": "Key", "Description": "Key Description"}, inplace=True
        )

        new["Key"] = new["Key"].str.strip()

        # update template file
        new.to_csv(os.path.join("./_data", term_csv_name + ".csv"), index=False)
        print("\033[92m {} \033[00m".format(f"Updated {term}.csv"))
    else:
        # convert dataframe to long format
        new = data_model.loc[data_model["Attribute"] == term,][
            ["Attribute", "Valid Values", "DependsOn", "Type", "Module"]
        ]
        new = (
            new.drop(columns=["Attribute", "DependsOn"])
            .set_index(["Type", "Module"])
            .apply(lambda x: x.str.split(",").explode())
            .reset_index()
        )
        # add columns
        new.rename(columns={"Valid Values": "Key"}, inplace=True)

        new["Key"] = new["Key"].str.strip()

        # load existing csv
        old = pd.read_csv(f"./_data/{term_csv_name}.csv")
        # upload existing csv if Key, Type or Module column is changed
        if not (
            new["Key"].equals(old["Key"])
            and new["Type"].equals(old["Type"])
            and new["Module"].equals(old["Module"])
        ):
            updated = new.astype(str).merge(
                old.astype(str), how="left", on=["Key", "Type", "Module"]
            )
            updated["Type"] = new["Type"]
            updated["Module"] = new["Module"]
            updated = updated[["Key", "Key Description", "Type", "Source", "Module"]]
            updated.to_csv(
                os.path.join("./_data", term_csv_name + ".csv"),
                index=False,
            )
            print("\033[92m {} \033[00m".format(f"Updated {term_csv_name}.csv"))


def manage_term_files(term=None):
    """_summary_

    Args:
        term (_type_, optional): _description_. Defaults to None.
    """

    # load data model
    data_model = pd.read_csv(config["data_model"])

    data_model["Attribute"] = data_model["Attribute"].str.replace(
        "\\s|/", "_", regex=True
    )

    # get the list of existing term csvs
    files = [
        file.split(".csv")[0] for file in os.listdir("_data/") if file.endswith(".csv")
    ]

    if term:
        df = data_model.loc[
            (data_model["Module"].notnull())
            & (
                data_model["Attribute"].isin(term)
                & (data_model["Parent"] != "validValue")
            )
        ]

    else:
        df = data_model.loc[data_model["Module"].notnull(),]

    # generate files when term files don't exist. Do not add files for valid values or specify because these have no useful sub values or depends on
    new_terms = df.loc[
        (~df["Attribute"].isin(files))
        & (df["Parent"] != "validValue")
        & (~df["Attribute"].str.contains("specify")),
        "Attribute",
    ].tolist()

    # generate csv by calling reformatter for each row of the df
    generate_csv_temp = partial(generate_csv, data_model)

    list(map(generate_csv_temp, new_terms))

    # update files if the term files exist
    exist_terms = df.loc[df["Attribute"].isin(files), "Attribute"].tolist()

    update_csv_temp = partial(update_csv, data_model)

    list(map(update_csv_temp, exist_terms))

    # delete term csv if the attribute is removed from data model
    for file in files:
        if file not in data_model.Attribute.values:
            os.remove(f"_data/{file}.csv")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "term",
        type=str,
        help="The term name(s) (Optional). Provide when you want to generate file(s) for specific term(s). Leave it blank if you want to edit files for all terms",
        nargs="*",
    )
    args = parser.parse_args()

    if args.term:
        manage_term_files(args.term)
    else:
        manage_term_files()


if __name__ == "__main__":
    main()

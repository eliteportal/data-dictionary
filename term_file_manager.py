"""
Name: term_file_manager.py
definition: a script to generate/update term csv 
parameters: term (str): the term name (optional)
Contributors: Dan Lu, Nicholas Lee

Notes: 
- CSV names cannot have spaces
"""
# load Parents
import argparse
import os
from functools import partial
import re
import pandas as pd
import yaml
import pathlib

with open("./_config.yml", "r") as f:
    config = yaml.safe_load(f)


def get_template_keys(data_model, template):
    """extract `dependsOn` values for the template

    Args:
        data_model (object): data model in use
        template (str): template attribute

    Returns:
        list: list of dependsOn terms
    """

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
    """Creates the term data frame csv to populate tables in the website.

    Args:
        data_model (object): full data model
        term (string): attribute term to look up

    Returns:
        object: data frame object
    """
    if "Template" in data_model.query("Attribute == @term")["Parent"].values:
        # generate csv for template
        depends_on = get_template_keys(data_model, term)

        # filter out attributes from data model table
        df = data_model.loc[data_model["Attribute"].isin(depends_on),]

        # # filter out valid values from data model table. data_model uses Parent to distinguish types of attributes
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
                "Parent",
            ]
        ].reset_index(drop=True)

        df.rename(
            columns={"Attribute": "Key", "Description": "Key Description"}, inplace=True
        )
    elif term == "countryCode":
        df = pd.read_excel(
            io="http://wits.worldbank.org/data/public/WITSCountryProfile-Country_Indicator_ProductMetada-en.xlsx",
            sheet_name="Country-Metadata",
        )

        df = df[
            ["Country Code", "Country Name", "Country ISO3", "Long Name", "Region"]
        ].rename({"Country Code": "Key", "Country Name": "Key Description"}, axis=1)

        df[
            "Source"
        ] = "https://wits.worldbank.org/countryprofile/metadata/en/country/all"
        df["Parent"] = "Metadata"
        df["Type"] = "Numeric"

    else:
        # prohibit = ["validValue", "BaseAnnotation", "Other"]
        df = data_model.loc[
            (~data_model["Valid Values"].isna()) | (~data_model["DependsOn"].isna()),
        ]

        df = df.loc[
            (df["Attribute"] == term) & (data_model["Parent"] != "validValue"),
        ][["Attribute", "Valid Values", "DependsOn", "Type", "Parent"]]

        # generate csv for term
        df = (
            df.drop(columns=["Attribute", "DependsOn"])
            .set_index(["Type", "Parent"])
            .apply(lambda x: x.str.split(",").explode())
            .reset_index()
        )

        # add columns
        df.rename(columns={"Valid Values": "Key"}, inplace=True)
        df = df.assign(**dict([(_, None) for _ in ["Key Description", "Source"]]))
        df = df[["Key", "Key Description", "Type", "Source", "Parent"]]

    return df


def generate_csv(data_model, term):
    """_summary_

    Args:
        data_model (_type_): _description_
        term (_type_): _description_
    """

    df = create_term_df(data_model, term)

    # need to make it readable
    term_csv_name = re.sub("\s|/", "_", term)

    # write out data frame
    df.to_csv(os.path.join("./_data", term_csv_name + ".csv"), index=False)

    print("\033[92m {} \033[00m".format(f"Added {term_csv_name}.csv"))


def update_csv(data_model, term):
    """_summary_

    Args:
        data_model (_type_): _description_
        term (_type_): _description_
    """
    term_csv_name = re.sub("\s|/", "_", term)

    if "Template" in data_model.query("Attribute == @term")["Parent"].values:
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
                "Parent",
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
            ["Attribute", "Valid Values", "DependsOn", "Type", "Parent"]
        ]
        new = (
            new.drop(columns=["Attribute", "DependsOn"])
            .set_index(["Type", "Parent"])
            .apply(lambda x: x.str.split(",").explode())
            .reset_index()
        )
        # add columns
        new.rename(columns={"Valid Values": "Key"}, inplace=True)

        new["Key"] = new["Key"].str.strip()

        # load existing csv
        old = pd.read_csv(f"./_data/{term_csv_name}.csv")
        # upload existing csv if Key, Type or Parent column is changed
        if not (
            new["Key"].equals(old["Key"])
            and new["Type"].equals(old["Type"])
            and new["Parent"].equals(old["Parent"])
        ):
            updated = new.astype(str).merge(
                old.astype(str), how="left", on=["Key", "Type", "Parent"]
            )
            updated["Type"] = new["Type"]
            updated["Parent"] = new["Parent"]
            updated = updated[["Key", "Key Description", "Type", "Source", "Parent"]]
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

    # remove spaces and irregular characters
    data_model["Attribute"] = data_model["Attribute"].str.replace(
        "\\s|/", "_", regex=True
    )

    # get the list of existing term csvs
    files = [
        file.split(".csv")[0] for file in os.listdir("_data/") if file.endswith(".csv")
    ]

    if term:
        df = data_model.loc[
            (~data_model["Attribute"].isin(files))
            & ((~data_model["Valid Values"].isna()) | (~data_model["DependsOn"].isna()))
            & (
                (~data_model["Attribute"].str.contains("specify"))
                | (~data_model["DependsOn"].str.contains("specify", na=False))
            ),
            "Attribute",
        ].tolist()

    else:
        df = data_model.loc[
            (~data_model["Valid Values"].isna()) | (~data_model["DependsOn"].isna()),
        ]

    # generate files when term files don't exist. Do not add files for valid values or specify because these have no useful sub values or depends on
    new_terms = df.loc[
        (~df["Attribute"].isin(files))
        & ((~data_model["Valid Values"].isna()) | (~data_model["DependsOn"].isna()))
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

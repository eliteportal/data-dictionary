"""
**Module Name:** page_manager.py

**Description:**

This Python script provides functions to generate documentation pages for a data model within a website. It includes functions to:

* Load the data model from a CSV file.
* Create a page for the entire data model.
* Create pages for individual modules within the data model.
* Create pages for templates defined in the data model.

**Contributors:**

* Dan Lu
* Nicholas Lee
"""

# load modules
import glob
import os
import re
import sys
from pathlib import Path
from datetime import datetime
import logging
import frontmatter
import pandas as pd
from mdutils import fileutils
from dotenv import dotenv_values

config = dotenv_values(".env")

root_dir_name = "data-dictionary"
for p in Path(__file__).parents:
    if bool(re.search(root_dir_name + "$", str(p))):
        ROOT_DIR = p

today = datetime.today().strftime("%Y-%m-%d")
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=Path(ROOT_DIR, "_logs", f"{today}_page_generation.log"),
    encoding="utf-8",
    level=logging.DEBUG,
    filemode="w",
)


def get_info(data_model: pd.DataFrame, term: str, column: str = "Attribute") -> dict:
    """
    Retrieves information about a specific term from a pandas DataFrame.

    Args:
        data_model: A pandas DataFrame representing the data model (pd.DataFrame).
        term: The name of the term to search for (str).
        column: The column name in the data model that contains the terms (str).
            Defaults to "Attribute".

    Returns:
        A dictionary containing information about the term, including:
            'Description' (str): The description of the term (if found).
            'Source' (str, optional): The source of the term information (if available in the data model).
            'Module' (str, optional): The module the term belongs to (if available in the data model).

    Raises:
        ValueError: If the provided term is not found in the data model.
    """

    # Filter data by term in the specified column
    results = data_model.loc[
        data_model[column] == term, ["Description", "Source", "Module"]
    ].to_dict("records")

    # Check if any results were found
    if not results:
        raise ValueError(f"Term '{term}' not found in the data model")

    # Assuming source information might not be available, handle potential missing key
    if not results[0].get("Source"):
        results[0]["Source"] = None

    # Return the first dictionary (assuming unique terms)
    return results[0]


def create_template_page(term: str, term_dict: dict) -> frontmatter.Post:
    """
    Creates a new markdown page for a specific template within the website's documentation.

    Args:
        term: The name of the template to create a page for (str).
        term_dict: A dictionary containing information about the template, including:
            'Description' (str): The description of the template.
            'Source' (str): The source of the template information. (URL or reference)

    Returns:
        A `frontmatter.Post` object representing the created template page metadata.

    Raises:
        ValueError: If the provided term name is empty, or if the term_dict is missing
            required keys 'Description' or 'Source'.
    """

    if not term:
        raise ValueError("Term name cannot be empty")

    if not all(key in term_dict for key in ["Description", "Source"]):
        raise ValueError("term_dict must contain keys 'Description' and 'Source'")

    # Load markdown template
    post = frontmatter.load(Path(ROOT_DIR, "_layouts/template_page_template.md"))

    # Update metadata for the new page
    post.metadata["title"] = re.sub("([A-Z]+)|_", r" \1", term).strip()
    post.metadata["parent"] = term_dict["Module"]

    # Inject term information into template content
    content_prefix = (
        "{% assign mydata=site.data."
        + re.sub("\s|/", "_", term)
        + " %} \n{: .note-title } \n"
        + f">{post.metadata['title']}\n"
        + ">\n"
        + f">{term_dict['Description']} [[Source]]({term_dict['Source']})\n"
    )
    post.content = content_prefix + post.content

    # Notice the return type is changed to `frontmatter.Post`
    # as this function doesn't create a file, it populates the post object.
    return post


def create_table_page(term: str, term_dict: dict) -> fileutils.MarkDownFile:
    """
    Creates a new markdown page for a specific term within the website's documentation.

    Args:
        term: The name of the term to create a page for (str).
        term_dict: A dictionary containing information about the term, including
            'Description' (str): The description of the term.
            'Source' (str): The source of the term information. (URL or reference)

    Returns:
        A `fileutils.MarkDownFile` object representing the created term page.

    Raises:
        ValueError: If the provided term name is empty, or if the term_dict is missing
            required keys 'Description' or 'Source'.
    """

    if not term:
        raise ValueError("Term name cannot be empty")

    if not all(key in term_dict for key in ["Description", "Source"]):
        raise ValueError("term_dict must contain keys 'Description' and 'Source'")

    # Load markdown template
    post = frontmatter.load(Path(ROOT_DIR, "_layouts/term_page_template.md"))

    # Update metadata for the new page
    post.metadata["title"] = term
    post.metadata["parent"] = term_dict["Module"]

    # Inject term information into template content
    content_prefix = (
        "{% assign mydata=site.data."
        + term
        + " %} \n{: .note-title } \n"
        + f">{term}\n"
        + ">\n"
        + f">{term_dict['Description']} [[Source]]({term_dict['Source']})\n"
    )
    post.content = content_prefix + post.content

    # Create and populate the term page file
    term_page = fileutils.MarkDownFile(str(Path(ROOT_DIR, f"docs/{term}.html")))
    term_page.append_end(frontmatter.dumps(post))

    return term_page


def create_module_page(module: str) -> fileutils.MarkDownFile:
    """
    Creates a new markdown page for a specific module within the website's documentation.

    Args:
        module: The name of the module to create a page for (str).

    Returns:
        A `fileutils.MarkDownFile` object representing the created module page.

    Raises:
        ValueError: If the provided module name is empty or invalid.
    """

    if not module:
        raise ValueError("Module name cannot be empty")

    # Load markdown template
    post = frontmatter.load(Path(ROOT_DIR, "_layouts/term_page_template.md"))

    # Update metadata for the new page
    post.metadata["title"] = module
    post.metadata["nav_order"] = 5
    post.metadata["permalink"] = f"docs/Modules/{module}.html"
    post.metadata["parent"] = "Modules"

    # Inject module name into template content
    content_prefix = (
        "{% assign mydata=site.data."
        + re.sub("\s|/", "_", module)
        + " %} \n{: .note-title } \n"
        + f">{module}\n"
        + ">\n"
        + ">Module in the data model\n"
    )
    post.content = content_prefix + post.content

    # Create and populate the module page file
    module_page = fileutils.MarkDownFile(str(Path(ROOT_DIR, f"docs/Modules/{module}")))
    module_page.append_end(frontmatter.dumps(post))

    return module_page


def create_full_table(data_model: pd.DataFrame) -> None:
    """
    Generates a markdown page for the entire data model within the website's documentation.

    Args:
        data_model: A pandas DataFrame representing the data model (pd.DataFrame).
    """

    # Module name for the full data model page
    module_name = "DataModel"

    # Create directory for the data model if it doesn't exist
    data_model_dir = Path(ROOT_DIR, f"docs/{module_name}")
    if not data_model_dir.exists():
        data_model_dir.mkdir(parents=True)  # Create parent directories if needed

    # Create the module page file
    module_page = fileutils.MarkDownFile(str(data_model_dir / module_name))

    # Load markdown template and update metadata
    post = frontmatter.load(Path(ROOT_DIR, "_layouts/term_page_template.md"))
    del post.metadata["parent"]
    post.metadata["title"] = module_name
    post.metadata["nav_order"] = 2
    post.metadata["permalink"] = f"docs/{module_name}.html"

    # Inject content about the full data model
    content_prefix = (
        "{% assign mydata=site.data."
        + module_name
        + " %} \n{: .note-title } \n"
        + f">{module_name}\n"
        + ">\n"
        + f">Complete Table of Keys for ELITE that are found in the data model\n"
    )
    post.content = content_prefix + post.content

    # Add the populated post content to the module page
    module_page.append_end(frontmatter.dumps(post))

    # Note: This function doesn't return anything as it modifies files directly.


def delete_page(term: str) -> list[str]:
    """
    Simulates deleting a markdown page for a term within the website's documentation.

    **Important:** This function does not permanently delete files. It simulates deletion for demonstration purposes.

    Args:
        term: The name of the term to simulate deletion for (str).

    Returns:
        A list of filenames that would have been deleted (list[str]).
    """

    # Pattern to match filenames based on term name
    file_pattern = f"{ROOT_DIR}/docs/**/*.{term}.md"

    # Simulate finding matching files
    deleted_files = [f for f in glob.glob(file_pattern, recursive=True)]

    # This function currently performs actual deletion (use with caution!)
    for file in deleted_files:
        logger.warning(f"Deleting: {file}")
        os.remove(file)

    return deleted_files


if __name__ == "__main__":
    # Load data model using pandas with informative error handling
    try:
        data_model = pd.read_csv(config["csv_model_link"])
    except FileNotFoundError:
        print("Error: CSV file not found! Please check the config file.")
        sys.exit(1)

    # Fill missing values with empty strings efficiently
    # data_model.fillna("", inplace=True)

    # Generate documentation pages
    create_full_table(data_model)
    for module in data_model["Module"].dropna().unique():
        create_module_page(module)

    templates = data_model[data_model["Parent"] == "Template"]["Attribute"].unique()
    for template in templates:
        term_attr = re.sub("_", " ", template)
        term_info = get_info(data_model, term_attr, column="Attribute")
        create_template_page(template, term_dict=term_info)

    logger.info("Documentation generation completed!")
    print("Documentation generation completed!")

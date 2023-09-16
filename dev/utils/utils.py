"""
Name: utils.py
definition: Useful functions
parameters: 
Contributors: Nicholas Lee

Notes: 
- 
"""

import datetime
import os
import pathlib

import pandas as pd
import numpy as np


def display_full_table(df: object):
    """Show data table without width restrictions

    Args:
        df (dataFrame): _description_
    """
    with pd.option_context("display.max_colwidth", None):
        display(df)


def get_time():
    """Create time stamp with format YYYY-MM-DD.Hr-Min

    Returns:
        string: current date and time
    """
    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime("%Y-%m-%d.%H-%M")
    return time_stamp


def load_and_backup_dm(file_path: str, output_path: str):
    """Create backup of data model with time stamp.

    Args:
        file_path (FILE): _description_

    Returns:
        object: Data frame object
    """

    dm = pd.read_csv(file_path, index_col=False)

    # write out old data model before changes
    time_stamp = get_time()

    dm.to_csv(output_path, index=False)

    return dm

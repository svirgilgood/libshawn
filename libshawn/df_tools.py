"""
Tools for interpreting dataframes 
"""

import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from typing import List


def clean_empty_rows(df: DataFrame | Series) -> DataFrame:
    """Cleans out empty rows in a dataframe. Rows that have None or Null or empty strings.
    This can cause problems with DataFrames, this function takes all of the typelical problems
    and replaces them with np.nan. Dropping them when they can."""
    new_df = pd.DataFrame(
        df.replace(r"\s+", " ", regex=True).apply(lambda x: x.str.strip())
    )
    new_df.replace("0", np.nan, inplace=True)
    new_df.replace("None", np.nan, inplace=True)
    new_df.replace("", np.nan, inplace=True)
    new_df.replace("  ", np.nan, inplace=True)
    new_df.replace("\n", np.nan, inplace=True)
    new_df.dropna(axis=1, how="all", inplace=True)
    return new_df


def deduplicate_dataframe(df: DataFrame, columns: List[str]) -> DataFrame:
    """Create a new DataFrame with only the unique values. The columns is the list of columns that
    Should be used for de duplication. These columns will be used to determine what is unique.
    """
    items = set()

    for _, row in df.iterrows():
        # print(row)
        items.add(tuple(row[col] for col in columns))
    new_dataframe = []
    for item in items:
        # I think there is a different way of doing this.
        # I should look into pandas documentation a bit more
        row = {key: value for key, value in zip(columns, item)}
        new_dataframe.append(row)
    return pd.DataFrame(new_dataframe)


def create_new_row_on_value(
    df: DataFrame, split_column: str, separator=";"
) -> DataFrame:
    """
    Pass a dataframe and split a column with a separator. Provide the name of the column to split on
    and the thing that separates the values on that column.
    """
    new_df = []
    for _, row in df.iterrows():
        try:
            new_values = row[split_column].split(separator)
        except AttributeError:
            new_values = [row[split_column]]
        for value in new_values:
            new_row = row.to_dict()
            new_row[split_column] = value
            new_df.append(new_row)
    return pd.DataFrame(new_df)

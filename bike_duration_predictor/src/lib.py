import pandas as pd
from typing import List


def convert_to_int(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Convert specified columns to integers and drop rows that cannot be converted.

    Args:
        df (pd.DataFrame): The input DataFrame.
        columns (List[str]): A list of column names to convert to integers.

    Returns:
        pd.DataFrame: The DataFrame with specified columns converted to integers and rows with NaN values in these columns dropped.
    """
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(subset=columns, inplace=True)

    for col in columns:
        df[col] = df[col].astype(int)

    return df


def map_membership_type(membership_type: str) -> str:
    """
    Map membership type strings to specified categories.

    Args:
        membership_type (str): The membership type string.

    Returns:
        str: The mapped category.
    """
    if pd.isna(membership_type):
        return 'Unknown'
    elif '365' in membership_type:
        return 'Annual Pass'
    elif '30 Day' in membership_type or 'Monthly' in membership_type:
        return 'Monthly Pass'
    elif 'Community Pass' in membership_type:
        return 'Community Pass'
    elif 'Pay Per Ride' in membership_type:
        return 'Pay Per Ride'
    else:
        return 'Other'


def one_hot_encode(df: pd.DataFrame, column: str, expected_columns: List[str]) -> pd.DataFrame:
    """
    Perform One-Hot Encoding on a specified column, map values to expected columns,
    and add missing columns if necessary.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column (str): The column to apply One-Hot Encoding to.
        expected_columns (List[str]): A list of expected columns after One-Hot Encoding.

    Returns:
        pd.DataFrame: The DataFrame with One-Hot Encoding applied.
    """
    df = pd.get_dummies(df, columns=[column])

    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    df[expected_columns] = df[expected_columns].astype(int)

    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names by converting them to lowercase, replacing spaces with underscores,
    and removing parentheses.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with standardized column names.
    """
    df.columns = df.columns.str.lower() \
        .str.replace(' ', '_') \
        .str.replace(r'[()]', '', regex=True)
    return df

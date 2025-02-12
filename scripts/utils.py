import pandas as pd


def split_at_char(df: pd.DataFrame, col: str, char: str):
    """_summary_

    Args:
        df (pd.DataFrame): DataFrame
        col (str): column name
        char (str): split character

    Returns:
        pd.DataFrame: returns the first index of the split
    """
    df[col] = df[col].astype(str).str.split(char).str[0]
    return df


def split_column_at(df: pd.DataFrame, col: str, char: str, index=0):
    return df[col].astype(str).str.split(char).str[index]


def replace_with(df: pd.DataFrame, col: str, term: str, replace_with: str):
    df[col] = df[col].str.replace(term, replace_with)
    return df

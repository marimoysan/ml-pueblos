import pandas as pd


def remove_big_cities(df: pd.DataFrame, size) -> pd.DataFrame:
    df = df.query(f"total_population < {size}")
    return df


def create_age_percentages(df: pd.DataFrame) -> pd.DataFrame:
    # Define age group columns
    age_groups = ["0-17", "18-24", "25-34", "35-54", "55+"]

    # Sum only the age group columns
    df["total_population"] = df[age_groups].sum(axis=1)

    # Compute percentages for each age group
    for col in age_groups:
        df[col + "_pct"] = (df[col] / df["total_population"]) * 100

    return df

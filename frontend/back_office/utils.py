import pandas as pd


def remove_big_cities(df: pd.DataFrame, size) -> pd.DataFrame:
    df = df.query(f"total_population < {size}")
    return df

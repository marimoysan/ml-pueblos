import pandas as pd
import numpy as np

accents = {
    "á": "a",
    "é": "e",
    "è": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "ñ": "n",
    "ü": "u",
    "¡": "i",
    "Á": "A",
    "É": "E",
    "È": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
    "Ñ": "N",
    "Ü": "U",
    "¿": "?",
}


class AccentCleaner:
    """A class to clean dataframes from any accents"""

    def __init__(
        self,
        dataframes: pd.DataFrame,
        columns: list[str],
        replacement_dict: dict = accents,
    ):
        self.dataframes = dataframes
        self.columns = columns
        self.replacement_dict = replacement_dict

    def __repr__(self) -> str:
        pass

    def cleanAccents(self):
        for df in self.dataframes:
            for column in self.columns:
                if column in df.columns:
                    df[column + "_clean"] = df[column].apply(
                        lambda x: "".join(
                            self.replacement_dict.get(c, c) for c in str(x)
                        ).lower()
                    )

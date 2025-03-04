import pandas as pd
import numpy as np
import re


class ColumnAligner:
    """A class to clean dataframes from any accents"""

    def __init__(self, boss: pd.DataFrame, minion: pd.DataFrame, column: str, pattern):
        self.boss = boss
        self.minion = minion
        self.column = column
        self.pattern = pattern

    def __repr__(self) -> str:
        pass

    def alignColumns(self):
        commas = self.boss.municipality_name_clean.str.contains(r".*, ")
        extract_list = self.boss[commas][self.column].str.split(",").str[0].to_list()

        for elem in extract_list:
            # Create a mask for rows in df_coordinates that contain the element
            mask = self.minion[self.column].str.contains(
                re.escape(elem) + r" \(", case=False, na=False
            )
            # # Get the corresponding full name from df_communities
            full_name = self.boss[
                self.boss[self.column].str.contains(f"{elem},", case=False, na=False)
            ][self.column].iloc[0]
            # Update df_coordinates with the full name where mask is True
            self.minion.loc[mask, self.column] = full_name

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
        pass

import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

# from sklearn.preprocessing import OneHotEncoder
# from sklearn.preprocessing import StandardScaler, MinMaxScaler
# from sklearn.pipeline import make_pipeline, Pipeline
# from sklearn.compose import ColumnTransformer

pd.set_option("display.max_columns", None)
# eye candy plots
plt.style.use(
    "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle"
)


def remove_big_cities(df: pd.DataFrame, size) -> pd.DataFrame:
    df = df.query(f"total_population < {size}")
    return df

import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.compose import ColumnTransformer

import streamlit as st

pd.set_option("display.max_columns", None)
# eye candy plots
plt.style.use(
    "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle"
)
st.set_page_config(page_title="Machine Learning", page_icon="📈")
st.sidebar.header("Machine Learning Demo")


if "df_select" not in st.session_state:
    st.session_state["df_select"] = pd.DataFrame()

if "columns" not in st.session_state:
    st.session_state["columns"] = pd.DataFrame()


ohe = OneHotEncoder(drop="first", sparse_output=False)
scaler = StandardScaler()

pipeline = Pipeline(steps=[("ohe", OneHotEncoder(drop="first", sparse_output=False))])

pipeline.fit(
    st.session_state["df_select"][["koppen_climate", "town_size", "final_age_category"]]
)

fe_transformer = ColumnTransformer(
    transformers=[
        ("transf_cat", pipeline, ["koppen_climate"])(
            "scaled",
            scaler,
            [
                "connectivity_score",
                "economy_score",
                "economy_score_area",
                "hospital_distance_score",
                "school_distance_score",
                "hospital_score_area",
                "school_score_area",
                "train_distance_score",
                "airport_distance_score",
                "transport_score",
            ],
        ),
    ],
    remainder="drop",
)

fe_transformer.fit(st.session_state["df_select"])

df_train = fe_transformer.transform(st.session_state["df_select"])

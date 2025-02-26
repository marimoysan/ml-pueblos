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
# Define default session state values
default_session_state = {
    "df_select": pd.DataFrame(),
    "columns": pd.DataFrame(),
    "another_key": "default_value",
}
# Initialize session state
for key, value in default_session_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.set_page_config(page_title="Machine Learning", page_icon="📈")
st.sidebar.header("Machine Learning Demo")


# Define categorical and numerical features based on the dataframe
categorical_features = st.session_state["columns"].columns.to_list()
numerical_features = (
    st.session_state["df_select"].select_dtypes(include=[np.number]).columns.tolist()
)

# Build the pipeline for the categorical transformations
pipeline = Pipeline(steps=[("ohe", OneHotEncoder(drop="first", sparse_output=False))])

# Create the column transformer using the pipelines defined above.
fe_transformer = ColumnTransformer(
    transformers=[
        ("transf_cat", pipeline, categorical_features),
        ("scaled", StandardScaler(), numerical_features),
    ],
    remainder="passthrough",
)

# Fit the transformer to the dataframe
fe_transformer.fit(st.session_state["df_select"])

df_train = fe_transformer.transform(st.session_state["df_select"])

st.dataframe(df_train)

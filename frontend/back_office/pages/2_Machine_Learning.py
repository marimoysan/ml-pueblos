import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import streamlit as st
from session_state_manager import initialize_session_state
from pipelines import Pipelines

st.set_page_config(page_title="Machine Learning", page_icon="📈")
st.sidebar.header("Machine Learning Demo")

initialize_session_state()
st.session_state["initial_run"] = False

pd.set_option("display.max_columns", None)
plt.style.use(
    "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle"
)

# Define categorical and numerical features based on the dataframe
categorical_features = st.session_state["df_cat_columns"].columns.to_list()
numerical_features = (
    st.session_state["df_select"].select_dtypes(include=[np.number]).columns.tolist()
)

pipelines = Pipelines()
feature_names, df = pipelines.build(
    st.session_state["df_select"],
    categorical_features,
    numerical_features,
)

df.columns = ["enc_" + feature_names[col] for col in df.columns]

st.session_state["df_train"] = df
st.dataframe(st.session_state.df_train)

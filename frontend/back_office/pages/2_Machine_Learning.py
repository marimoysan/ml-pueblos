import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import streamlit as st

pd.set_option("display.max_columns", None)
# eye candy plots
plt.style.use(
    "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle"
)
default_session_state = {
    "df_select": pd.DataFrame(),
    "df_cat_columns": pd.DataFrame(),
    "df_train": pd.DataFrame(),
    "df_origin": pd.DataFrame(),
    "initial_run": False,
}
# Initialize session state
for key, value in default_session_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.set_page_config(page_title="Machine Learning", page_icon="📈")
st.sidebar.header("Machine Learning Demo")


# Define categorical and numerical features based on the dataframe
categorical_features = st.session_state["df_cat_columns"].columns.to_list()
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
    remainder="drop",
)

# Fit the transformer to the dataframe
fe_transformer.fit(st.session_state["df_select"])
df = pd.DataFrame(fe_transformer.transform(st.session_state["df_select"]))

df.columns = ["enc_" + str(col) for col in df.columns]


st.session_state["df_train"] = df


st.dataframe(st.session_state.df_train)

# if st.button("Save DataFrame to CSV"):
#     pd.DataFrame(st.session_state["df_train"]).to_csv(
#         "../../data/interim/training_data.csv"
#     )

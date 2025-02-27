import streamlit as st
import pandas as pd
import numpy as np
from session_state_manager import initialize_session_state

st.set_page_config(page_title="Feature Engineering", page_icon="📈")
initialize_session_state()
st.session_state["initial_run"] = False

st.sidebar.header("Feature Engineering")
st.title("Feature Engineering")

st.write("### Current DataFrame")
st.write(st.session_state["df_select"])

st.write(f"New shape:")
st.write(st.session_state["df_select"].shape)

st.write("---")
st.write("### Which categorical columns should be transformed with OneHotEncoder?")

categorical_columns = (
    st.session_state["df_select"]
    .select_dtypes(include=[pd.CategoricalDtype(), np.object_])
    .columns.tolist()
)

for elem in categorical_columns:
    checkbox_state = st.checkbox(label=f"{elem}", key=f"fe_{elem}")
    if checkbox_state:
        st.session_state["df_cat_columns"][elem] = st.session_state["df_select"][elem]
    else:
        if elem in st.session_state["df_cat_columns"]:
            st.session_state["df_cat_columns"].drop(columns=[elem], inplace=True)


st.write(st.session_state["df_cat_columns"])
st.write(f"New shape:")
st.write(st.session_state["df_select"].shape)

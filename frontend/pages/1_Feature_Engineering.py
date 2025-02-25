import os
import streamlit as st
import pandas as pd
import io
import math

st.set_page_config(page_title="Feature Engineering", page_icon="📈")
st.sidebar.header("Feature Engineering")

st.title("Feature Engineering")

if "df_select" not in st.session_state:
    st.session_state["df_select"] = pd.DataFrame()

st.session_state["df"] = pd.DataFrame()

st.write("### Current DataFrame")
st.write(st.session_state["df_select"])

st.write("### Which columns should be transformed with OneHotEncoder?")

columns = st.session_state["df_select"].columns.to_list()

st.write(columns)

layout_cols = st.columns(4)

for i in columns:
    if st.checkbox(f"{i}", key=i):
        st.session_state["df"][i] = st.session_state["df_select"][i]

st.markdown("<br><br>", unsafe_allow_html=True)
if not st.session_state["df"].empty:
    st.dataframe(st.session_state["df"].sample(5))

if st.button("Save DataFrame to CSV"):
    st.session_state["df"].to_csv("../data/output/streamlined.csv")

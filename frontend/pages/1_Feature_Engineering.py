import os
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Feature Engineering", page_icon="📈")
st.sidebar.header("Feature Engineering")

if "df_select" not in st.session_state:
    st.session_state["df_select"] = pd.DataFrame()

st.write(st.session_state["df_select"])

buffer = io.StringIO()
st.session_state["df_select"].info(buf=buffer)
df_info = buffer.getvalue()
st.text(df_info)

if st.button("Save DataFrame to CSV"):
    st.session_state["df_select"].to_csv("../data/output/streamlined.csv")

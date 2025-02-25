import streamlit as st
import pandas as pd

st.set_page_config(page_title="Feature Engineering", page_icon="📈")
st.sidebar.header("Feature Engineering")

st.title("Feature Engineering")

if "df_select" not in st.session_state:
    st.session_state["df_select"] = pd.DataFrame()

if "columns" not in st.session_state:
    st.session_state["columns"] = pd.DataFrame()

st.write("### Current DataFrame")
st.write(st.session_state["df_select"])

st.write(f"New shape:")
st.write(st.session_state["df_select"].shape)

st.write("---")
st.write("### Which categorical columns should be transformed with OneHotEncoder?")

for elem in st.session_state["df_select"].columns.to_list():
    checkbox_state = st.checkbox(f"{elem}", key=f"fe_{elem}")
    if checkbox_state:
        st.session_state["columns"][elem] = st.session_state["df_select"][elem]
    else:
        if elem in st.session_state["columns"]:
            st.session_state["columns"].drop(columns=[elem], inplace=True)


st.write(st.session_state["columns"])
st.write(f"New shape:")
st.write(st.session_state["df_select"].shape)

if st.button("Save DataFrame to CSV"):
    st.session_state["columns"].to_csv("../data/output/ohe_marked.csv")

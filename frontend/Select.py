import os
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Select Columns",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

if "df_select" not in st.session_state:
    st.session_state["df_select"] = pd.DataFrame()

st.sidebar.success("Select Columns")

# Set the working directory to the script's location and configure page
os.chdir(os.path.dirname(os.path.abspath(__file__)))
st.write("## Los Pueblos")

import streamlit as st
import math


csv_path = "../data/processed/3_aggregated_pueblos.csv"
df = pd.read_csv(csv_path)

cb_show = st.checkbox(f"Show DataFrame")
if cb_show:
    st.dataframe(df)

st.write("### Which columns would you like to incorporate for clustering?")

columns = df.columns.to_list()
layout_cols = st.columns(4)
chunk_size = math.ceil(len(columns) / len(layout_cols))
chunks = [columns[i : i + chunk_size] for i in range(0, len(columns), chunk_size)]

for i in range(len(layout_cols)):
    with layout_cols[i]:
        for elem in chunks[i]:
            if st.checkbox(f"{elem}", key=elem):
                st.session_state["df_select"][elem] = df[elem]


# selections = st.multiselect("Choose Columns", list(df.columns), [])
# st.write(selections)


st.markdown("<br><br>", unsafe_allow_html=True)
if not st.session_state["df_select"].empty:
    st.dataframe(st.session_state["df_select"].sample(5))

if st.button("Save DataFrame to CSV"):
    st.session_state["df_select"].to_csv("../data/output/streamlined.csv")

import os
import streamlit as st
import pandas as pd
import math
from utils import remove_big_cities

import streamlit as st

st.set_page_config(
    page_title="Select Columns",
    page_icon="👋",
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
st.title("Los Pueblos")


csv_path = "../data/processed/3_aggregated_pueblos.csv"
df = pd.read_csv(csv_path)


village_size = st.slider(
    "Village size: ", min_value=500, max_value=10000, value=6000, step=500
)

is_small = st.checkbox(f"Remove cities larger than {village_size} people?")
restore_df = df.copy()
if is_small:
    df = remove_big_cities(df, village_size)
    st.write(f"New shape: {df.shape}")
else:
    df = restore_df
    st.write(f"New shape: {df.shape}")

st.markdown("---")

# Define age group columns
age_groups = ["0-17", "18-24", "25-34", "35-54", "55+"]

# Sum only the age group columns
df["total_population"] = df[age_groups].sum(axis=1)

# Compute percentages for each age group
for col in age_groups:
    df[col + "_pct"] = (df[col] / df["total_population"]) * 100


cb_show = st.checkbox(f"Show DataFrame")
if cb_show:
    st.dataframe(df)
    st.write(f"New shape: {df.shape}")

st.write("### Which columns would you like to incorporate for clustering?")

columns = df.columns.to_list()
layout_cols = st.columns(3)
chunk_size = math.ceil(len(columns) / len(layout_cols))
chunks = [columns[i : i + chunk_size] for i in range(0, len(columns), chunk_size)]

for i in range(len(layout_cols)):
    with layout_cols[i]:
        for elem in chunks[i]:
            if st.checkbox(f"{elem}", key=elem):
                st.session_state["df_select"][elem] = df[elem]
            else:
                if elem in st.session_state["df_select"]:
                    st.session_state["df_select"].drop(columns=[elem], inplace=True)

st.markdown("---")
if not st.session_state["df_select"].empty:
    st.dataframe(st.session_state["df_select"])
    st.write(f"New shape:")
    st.write(st.session_state["df_select"].shape)

if st.button("Save DataFrame to CSV"):
    st.write(f"New shape:")
    st.write(st.session_state["df_select"].shape)
    st.session_state["df_select"].to_csv("../data/output/streamlined.csv")

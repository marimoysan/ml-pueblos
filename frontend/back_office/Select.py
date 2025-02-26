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

default_session_state = {
    "df_select": pd.DataFrame(),
    "df_cat_columns": pd.DataFrame(),
    "df_train": pd.DataFrame(),
    "df_origin": pd.DataFrame(),
    "initial_run": True,
}

# Initialize session state
for key, value in default_session_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.sidebar.success("Select Columns")

# Set the working directory to the script's location and configure page
os.chdir(os.path.dirname(os.path.abspath(__file__)))
st.title("Los Pueblos")


csv_path = "../../data/end-product-data/pueblos_input.csv"
st.session_state["df_origin"] = pd.read_csv(csv_path)


village_size = st.sidebar.slider(
    "Village size: ", min_value=500, max_value=10000, value=6000, step=500
)

is_small = st.sidebar.checkbox(
    f"Remove cities larger than {village_size} people?", value=True
)
restore_df = st.session_state["df_origin"].copy()
if is_small:
    st.write("Is small")
    st.session_state["df_origin"] = remove_big_cities(
        st.session_state["df_origin"], village_size
    )
    st.write(f"Shape: {st.session_state['df_origin'].shape}")
else:
    st.session_state["df_origin"] = restore_df
    st.write(f"Shape: {st.session_state['df_origin'].shape}")

st.markdown("---")

# Define age group columns
age_groups = ["0-17", "18-24", "25-34", "35-54", "55+"]

# Sum only the age group columns
st.session_state["df_origin"]["total_population"] = st.session_state["df_origin"][
    age_groups
].sum(axis=1)

# Compute percentages for each age group
for col in age_groups:
    st.session_state["df_origin"][col + "_pct"] = (
        st.session_state["df_origin"][col]
        / st.session_state["df_origin"]["total_population"]
    ) * 100

cb_show = st.checkbox(f"Show DataFrame")
if cb_show:
    st.dataframe(st.session_state["df_origin"])
    st.write(f"New shape: {st.session_state['df_origin'].shape}")

st.write("### **Which columns would you like to incorporate for clustering?**")

columns = st.session_state["df_origin"].columns.to_list()
layout_cols = st.columns(3)
chunk_size = math.ceil(len(columns) / len(layout_cols))
chunks = [columns[i : i + chunk_size] for i in range(0, len(columns), chunk_size)]


if st.session_state.initial_run:
    selection_defaults = [
        "province",
        "total_population",
        "koppen_climate",
        "connectivity_category",
        "economy_score",
    ]
else:
    selection_defaults = st.session_state["df_select"].columns.to_list()

for i in range(len(layout_cols)):
    with layout_cols[i]:
        for elem in chunks[i]:
            checkbox_state = st.checkbox(
                f"{elem}", key=elem, value=(elem in selection_defaults)
            )
            if checkbox_state:
                st.session_state["df_select"][elem] = st.session_state["df_origin"][
                    elem
                ]
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
    st.session_state["df_select"].to_csv("../../data/interim/streamlined.csv")

st.session_state.initial_run = False

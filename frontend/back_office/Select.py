import os
import streamlit as st
import pandas as pd
import math
from session_state_manager import initialize_session_state, reset_session_state
import streamlit as st
from utils import remove_big_cities, create_age_percentages

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

initialize_session_state()

# Set the working directory to the script's location and configure page
os.chdir(os.path.dirname(os.path.abspath(__file__)))
st.title("Los Pueblos")


csv_path = "../../data/end-product-data/input_clusterer.csv"

# TODO only taking a fraction of the df for now

df_origin = pd.read_csv(csv_path)
df_origin = df_origin.iloc[::5]

st.session_state["df_origin"] = df_origin

village_size = st.sidebar.slider(
    "Village size: ", min_value=500, max_value=10000, value=6000, step=500
)

is_small = st.sidebar.checkbox(
    f"Remove cities larger than {village_size} people?", value=True
)

restore_df = st.session_state["df_origin"].copy()

if is_small:
    st.session_state["df_origin"] = remove_big_cities(
        st.session_state["df_origin"], village_size
    )
    st.write(f"Shape: {st.session_state['df_origin'].shape}")
else:
    st.session_state["df_origin"] = restore_df
    st.write(f"Shape: {st.session_state['df_origin'].shape}")

st.markdown("---")

st.session_state["df_origin"] = create_age_percentages(st.session_state["df_origin"])

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
        "final_age_category",
        "town_size",
        "economy_score_area",
        "hospital_score_area",
        "school_score_area",
        "transport_score",
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

# if st.button("Save DataFrame to CSV"):
#     st.write(f"New shape:")
#     st.write(st.session_state["df_select"].shape)
#     st.session_state["df_select"].to_csv("../../data/interim/streamlined.csv")

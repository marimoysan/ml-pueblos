import os
import streamlit as st
from streamlit_card import card
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))
st.set_page_config(layout="wide")
st.write("## Los Pueblos")
st.text("Please select your preferred village")


csv_path = "../data/output/pueblos.csv"
df = pd.read_csv(csv_path)

clusters = df["cluster_kmeans"].unique()
cols = st.columns(len(clusters))

with cols[0]:
    with st.form("Form1"):
        if "df_1" not in st.session_state:
            st.session_state.df_1 = df.loc[df["cluster_kmeans"] == 0].sample(1)

        df_1 = st.session_state.df_1
        municipality_1 = df_1.iloc[0]["municipality"]

        flavor = st.selectbox("Select flavor", ["Vanilla", "Chocolate"], key="flav")
        intensity1 = st.slider(
            label="Select intensity", min_value=0, max_value=100, key="intens1"
        )
        st.dataframe(df_1, key="df_1")
        municipality_1 = df_1.iloc[0]["municipality"]
        st.markdown(
            f"<u><b style='font-size: 18px'>{municipality_1}</b></u>",
            unsafe_allow_html=True,
        )
        submitted1 = st.form_submit_button("Submit 1")
    if submitted1:
        st.dataframe(df_1)
        st.write(municipality_1)
        st.write(f"Form1 submitted. Flavor: {flavor} | Intensity: {intensity1}")

        # df_1.to_csv("../data/output/test.csv")


with cols[1]:
    with st.form("Form2"):
        if "df_2" not in st.session_state:
            st.session_state.df_2 = df.loc[df["cluster_kmeans"] == 0].sample(1)
        df_2 = st.session_state.df_2
        municipality_2 = df_2.iloc[0]["municipality"]

        topping = st.selectbox("Select Topping", ["Almonds", "Sprinkles"], key="top")
        intensity2 = st.slider(
            label="Select Intensity", min_value=0, max_value=100, key="intens2"
        )
        st.dataframe(df_2, key="df_2")
        municipality_2 = df_2.iloc[0]["municipality"]
        st.markdown(
            f"<u><b style='font-size: 18px'>{municipality_2}</b></u>",
            unsafe_allow_html=True,
        )
        submitted2 = st.form_submit_button("Submit 2")
    if submitted2:
        st.write(municipality_2)
        st.write(f"Form2 submitted. Topping: {topping} | Intensity: {intensity2}")

        # df_2.to_csv("../data/output/test.csv")

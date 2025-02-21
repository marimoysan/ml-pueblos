import os
import streamlit as st
from streamlit_card import card
import pandas as pd

# Set the working directory to the script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))
st.set_page_config(layout="wide")

st.write("## Los Pueblos")
st.text("Please select your preferred village")

# CSV file path and reading the data
csv_path = "../data/output/pueblos.csv"
df = pd.read_csv(csv_path)

# Sidebar header for cluster selection (for possible future use)
# st.sidebar.header("Please select a village you would prefer!")

# Get unique clusters from the dataframe column
clusters = df["cluster_kmeans"].unique()

# Create a row of columns; one column per card
cols = st.columns(len(clusters))

# Loop over each cluster and sample one town to display in a card
for col, idx in zip(cols, clusters):
    df_current = df.loc[df["cluster_kmeans"] == idx].sample(1)
    # st.dataframe(df_current)

    municipality = df_current.iloc[0]["municipality"]
    population = df_current.iloc[0]["total_population"]
    province = df_current.iloc[0]["province"]

    with col:
        card(
            title=municipality,
            text=f"Population: {population}  |  Province: {province}  |  Population: {population}",
            on_click=lambda: st.write(f"Selected: {municipality}"),
            styles={
                "card": {
                    "width": "auto",
                    "height": "300px",
                    "border-radius": "10px",
                    "box-shadow": "0 2px 10px rgba(0,0,0,0.25)",
                    "background-color": "#649AA7",
                    "margin": "5px",
                    "padding": "10px",
                },
                "text": {
                    "font-family": "Arial",
                    "color": "#FFF",
                    "font-size": "12px",
                    "text-align": "center",
                },
                "title": {
                    "font-family": "Arial",
                    "color": "#FFF",
                    "font-size": "20px",
                    "font-weight": "bold",
                    "text-align": "center",
                },
            },
        )

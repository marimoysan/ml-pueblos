import os
import streamlit as st
from streamlit_card import card
import pandas as pd


# Set the working directory to the script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

st.write(
    """
# Los Pueblos
"""
)

# Ensure the correct path to the CSV file
csv_path = "../data/output/pueblos.csv"

# Read the CSV file
df = pd.read_csv(csv_path)
# Add a sidebar for user input
st.sidebar.header("Select Cluster")

# Get unique values for the selection
clusters = df["cluster_kmeans"].unique()

# # Create multiselect widgets for filtering
# selected_cluster = st.sidebar.multiselect("Select Clusters", clusters)

# # Filter the dataframe based on user selection
# filtered_df = df[(df["cluster_kmeans"].isin(selected_cluster))]

# # Display the filtered data
# st.write("## Filtered Data")
# st.dataframe(filtered_df)

# hasClicked = card(
#     title="Hello World!",
#     text="Some description",
#     image="http://placekitten.com/200/300",
#     on_click=lambda: print("Clicked!"),
# )

# # Display cards for selection
# st.write("## Pueblo Cards")
# for elem in selected_cluster:
#     elem_data = filtered_df[filtered_df["cluster_kmeans"] == elem]
#     for index, row in elem_data.iterrows():
#         card(title=f"{row['municipality']}", text=f"{row['total_population']}")


for idx in clusters:
    df_current = df.loc[df["cluster_kmeans"] == idx].sample(1)
    st.dataframe(df_current)
    card(
        title=f"{df_current.iloc[0]['municipality']}",
        text=f"Population: {df_current.iloc[0]['total_population']}",
        # image="http://placekitten.com/200/300",
        on_click=lambda: print("Clicked!"),
    )

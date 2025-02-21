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

# Initialize session state for storing dataframe values if not already present
if "selected_villages" not in st.session_state:
    st.session_state.setdefault("selected_villages", pd.DataFrame(columns=df.columns))
    st.session_state.setdefault("counter", 0)

if st.session_state.counter < 5:
    st.session_state.counter += 1

    for col, idx in zip(cols, clusters):
        df_current = df.loc[df["cluster_kmeans"] == idx].sample(1)
        # st.dataframe(df_current)

        municipality = df_current.iloc[0]["municipality"]
        population = df_current.iloc[0]["total_population"]
        province = df_current.iloc[0]["province"]
        internet = df_current.iloc[0]["connectivity_category"]
        climate = df_current.iloc[0]["description"]

        with col:
            with st.form(str(idx)):
                st.markdown(
                    f"<u><b style='font-size: 18px'>{municipality}</b></u>",
                    unsafe_allow_html=True,
                )
                st.write(f"Population: {population}")
                st.write(f"Province: {province}")
                st.write(f"Connectivity: {internet}")
                st.write(f"Climate: {climate}")
                # Every form must have a submit button.
                submitted = st.form_submit_button("Choose")

                ######## This is just a test ##################
                ######## This is just a test ##################
                ######## This is just a test ##################
                ######## This is just a test ##################

                if submitted:
                    # Add the current row to the session state dataframe
                    st.session_state.selected_villages = pd.concat(
                        [st.session_state.selected_villages, df_current]
                    )
                    df_current.to_csv("../data/output/test.csv")

else:
    st.write("# Thank you for your preferences!")
    # Display the selected villages
    st.write("## Selected Villages")
    st.dataframe(st.session_state.selected_villages)

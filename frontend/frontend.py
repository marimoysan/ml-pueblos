import os
import streamlit as st
import pandas as pd

# Set the working directory to the script's location and configure page
os.chdir(os.path.dirname(os.path.abspath(__file__)))
st.set_page_config(layout="wide")
st.write("## Los Pueblos")
st.text("Please select your preferred village")

# CSV file path for input and output
csv_path = "../data/output/pueblos.csv"
output_csv_path = "../data/output/selected_villages.csv"
df = pd.read_csv(csv_path)

# Get unique cluster IDs from the dataframe (assumes clusters are numeric)
clusters = sorted(df["cluster_kmeans"].unique())


# Function to load new samples
def load_samples():
    samples = {}
    for cl in clusters:
        samples[cl] = df.loc[df["cluster_kmeans"] == cl].sample(1)
    return samples


# Create samples only once and store in session_state to avoid re-sampling on every run.
if "samples" not in st.session_state:
    st.session_state["samples"] = load_samples()

# Create a row of columns—one for each cluster sample
cols = st.columns(len(clusters))

# Loop over each sample (keyed by cluster id)
for cl, col in zip(clusters, cols):
    # Retrieve the sample from session_state
    sample_df = st.session_state["samples"][cl]
    row = sample_df.iloc[0]
    municipality = row["municipality"]
    population = row["total_population"]
    province = row["province"]
    connectivity = row["connectivity_category"]
    climate = row["description"]

    with col:
        st.markdown(
            f"""<div style="border:1px solid #ccc; border-radius:8px; padding:16px; background-color:#f9f9f9">
            <h3 style="text-decoration:underline; font-size:18px;">{municipality}</h3>
            <p>Population: {population}</p>
            <p>Province: {province}</p>
            <p>Connectivity: {connectivity}</p>
            <p>Climate: {climate}</p>
            </div>""",
            unsafe_allow_html=True,
        )
        # Each card has its own selection button
        if st.button(f"Choose {municipality}", key=f"choose_{cl}"):
            # Append the chosen sample to the output CSV file.
            # Use header only if the file does not exist.
            sample_df.to_csv(
                output_csv_path,
                mode="a",
                index=False,
                header=not os.path.exists(output_csv_path),
            )
            st.success(f"Appended {municipality} to CSV!")
            # Load new samples
            st.session_state["samples"] = load_samples()

st.write("### Thank you for your preferences!")

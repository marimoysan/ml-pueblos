import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import random
import uuid


def show():
    menu_items = (
        {
            "Get Help": "https://www.extremelycoolapp.com/help",
            "Report a bug": "https://www.extremelycoolapp.com/bug",
            "About": "# This is a header. This is an *extremely* cool app!",
        },
    )

    # CSV file path for input and output
    # csv_path = "../../data/end-product-data/pueblos_backoffice.csv"
    csv_path = "../../data/end_product_data/pueblos_recommender.csv"  ## we would change it to original_df + onehote...
    output_csv_path = f"../../data/user_output/{uuid.uuid4().hex}.csv"

    df = pd.read_csv(csv_path)

    if "output_path" not in st.session_state:
        st.session_state["output_path"] = output_csv_path

    st.write(st.session_state["output_path"])
    st.write("## So, if you would have these options, where would you like to live?")
    st.text("Think carefully...")

    # Get unique cluster IDs from the dataframe (assumes clusters are numeric)
    cluster_ids = sorted(df["cluster"].unique())

    # Function to load new samples
    def load_samples():
        samples = {}
        for cl in cluster_ids:
            samples[cl] = df.loc[df["cluster"] == cl].sample(1)
        return samples

    # Create samples only once and store in session_state to avoid re-sampling on every run.
    if "samples" not in st.session_state:
        st.session_state["samples"] = load_samples()
        st.session_state.collected_df = []
        st.session_state["counter"] = 0

    options_samples = pd.concat(
        list(st.session_state["samples"].values()), ignore_index=True
    )

    # Define the map layer
    scatter_options = pdk.Layer(
        "ScatterplotLayer",
        data=options_samples,
        get_position=["longitude", "latitude"],
        get_radius=15000,  # Size of the points (adjust as needed)
        get_color="[255, 0, 0, 150]",  # Red color with some transparency
        pickable=True,  # Enables hover tooltips
    )

    # define the initial view state for Spain (Peninsula)
    view_state = pdk.ViewState(
        latitude=40.0,  # Center over Spain
        longitude=-3.5,  # Near Madrid for a balanced view
        zoom=5,  # Zoom level to fit all of Spain
        min_zoom=5,
        max_zoom=5,
        pitch=0,  # Top-down view
        draggable=False,
    )

    # Define tooltips with more details
    tooltip = {
        "html": """
        <div style="font-size:14px; padding:5px;">
            <b>🏡 Municipality:</b> {municipality}<br>
            <b>🌍 Province:</b> {province}<br>
            <b>👥 Population:</b> {total_population}<br>
            <b>📡 Connectivity:</b> {category_connectivity}<br>
            <b>🌤️ Climate:</b> {description}
        </div>
        """,
        "style": {
            "backgroundColor": "white",
            "color": "black",
            "padding": "10px",
            "borderRadius": "8px",
        },
    }

    # Create the pydeck chart
    st.pydeck_chart(
        pdk.Deck(
            layers=[scatter_options],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style="mapbox://styles/mapbox/light-v9",  # Change map style (light, dark, satellite, etc.)
        )
    )

    # Create a row of columns— one for each cluster sample
    cols = st.columns(len(cluster_ids))

    if st.session_state.counter < 5:
        # Loop over each sample (keyed by cluster id)
        for cl, col in zip(cluster_ids, cols):
            # Retrieve the sample from session_state
            sample_df = st.session_state["samples"][cl]
            row = sample_df.iloc[0]
            municipality = row["municipality"]
            population = row["total_population"]
            province = row["province"]
            connectivity = row["category_connectivity"]
            climate = row["description"]

            with col:
                # Each card has its own selection button
                st.markdown(
                    """
                    <style>
                    div.stButton > button {
                        width: 240px;
                        background: #f9f9f9 !important;
                        color: black !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(f"{municipality}", key=f"choose_{cl}"):
                    # if st.button(f"Choose {municipality}", key=f"choose_{cl}"):
                    st.session_state.collected_df.append(sample_df)
                    # Load new samples
                    st.session_state["samples"] = load_samples()
                    st.session_state.counter += 1
                    st.rerun()

    else:
        pd.concat(st.session_state.collected_df, ignore_index=True).to_csv(
            st.session_state.output_path,
            mode="a",
            index=False,
            header=not os.path.exists(output_csv_path),
        )
        st.write("thanks")
        st.session_state.page = "get_recommendations"
        st.rerun()  # Reload the app to show the main page


## user selection:
# five rows with 5 selected towns. original data + ohe

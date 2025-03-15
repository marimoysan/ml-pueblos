import streamlit as st
import pandas as pd
import pydeck as pdk
import uuid
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity


def render_svd_sparse(user_choices, df_pueblos):
    # Dimensionality Reduction & Similarity Calculation
    sparse_matrix = user_choices.filter(regex=r"^enc_", axis=1).values
    svd = TruncatedSVD(n_components=4)
    user_latent_features = svd.fit_transform(sparse_matrix)
    pueblos_latent_features = svd.transform(
        df_pueblos.filter(regex=r"^enc_", axis=1).values
    )

    # Compute similarities
    similarities = cosine_similarity(user_latent_features, pueblos_latent_features)
    df_pueblos["similarity"] = similarities.mean(axis=0)
    df_towns = df_pueblos.sort_values(by="similarity", ascending=False).head(5)

    for _, row in df_towns.iterrows():
        municipality = row["municipality"]
        province = row["province"]
        similarity = round(row["similarity"] * 100, 1)
        population = f"{row['total_population']:,}"
        connectivity = row["category_connectivity"]
        transport = row["category_transport"]

        # Create a small map for each town (with Spain as the main view)
        town_map_data = pd.DataFrame(
            {
                "latitude": [row["latitude"]],
                "longitude": [row["longitude"]],
            }
        )

        town_layer = pdk.Layer(
            "ScatterplotLayer",
            data=town_map_data,
            get_position=["longitude", "latitude"],
            get_radius=15000,  # Size of the points (adjust as needed)
            get_color="[255, 0, 0, 150]",  # Red color with some transparency
            pickable=True,
        )

        # Set view state to Spain, ensuring a full-country perspective
        town_view_state = pdk.ViewState(
            latitude=40.0,  # Center of Spain
            longitude=-3.5,  # Roughly Madrid
            zoom=5,  # Zoomed out to see the whole country
            pitch=0,
        )

        # Layout with map and text side by side
        col1, col2 = st.columns([1, 2])

        with col1:
            st.pydeck_chart(
                pdk.Deck(
                    layers=[town_layer],
                    initial_view_state=town_view_state,
                    height=150,
                )
            )

        with col2:
            st.markdown(
                f"""
                <div style="
                    border-radius: 10px; 
                    padding: 15px; 
                    margin: 10px 0px; 
                    background-color: #1e1e1e;  /* Dark background */
                    border-left: 5px solid #4A90E2; /* Blue accent */
                    color: #ffffff;  /* White text */
                ">
                    <h4 style="margin: 0px; color: #ffffff;">{municipality}, {province}</h4>
                    <p style="margin:0px; color: #dddddd;">
                    <b>Similarity Score:</b> {similarity}%<br> </p></br>
                    <p style="margin: 5px 0px; color: #dddddd;">
                        👥 <b>Population:</b> {population}<br>
                        📡 <b>Connectivity:</b> {connectivity}<br>
                        🚆 <b>Transport:</b> {transport}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 🔹 Like & Dislike Buttons (Aligned Right)
        with st.container():
            _, col_btn1, col_btn2 = st.columns(
                [0.83, 0.08, 0.1]
            )  # More space on the left

            with col_btn1:
                st.button("👍 Like", key=f"like_{uuid.uuid4()}")

            with col_btn2:
                st.button("👎 Dislike", key=f"dislike_{uuid.uuid4()}")

        st.write("---")

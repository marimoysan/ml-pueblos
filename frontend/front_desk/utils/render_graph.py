from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import streamlit as st
import numpy as np
import pandas as pd
import pickle
import pydeck as pdk
import uuid


def render_graph(user_choices, df_pueblos):
    svd = TruncatedSVD(n_components=5)
    user_choices_cmun = user_choices.cmun.tolist()
    G, model = _load_graph_model()

    df_similarities = _calc_similarities(G, model, svd, user_choices_cmun)
    # Convert df_similarities to the ranked_villages format that ndcg_at_k expects
    _rank_villages(df_pueblos, df_similarities)


def _rank_villages(df_pueblos, df_similarities):
    # Merge similarity data with town information
    df_towns = pd.merge(
        df_similarities.sort_values(by="similarity", ascending=False).head(5),
        df_pueblos,
        on="cmun",
        how="inner",
    )

    # Display each recommended town
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

        # Like & Dislike Buttons (Aligned Right)
        with st.container():
            _, col_btn1, col_btn2 = st.columns(
                [0.83, 0.08, 0.1]
            )  # More space on the left

            with col_btn1:
                st.button("👍 Like", key=f"like_{uuid.uuid4()}")

            with col_btn2:
                st.button("👎 Dislike", key=f"dislike_{uuid.uuid4()}")

        st.write("---")


def _load_graph_model():
    model_path = "../../models/node2vec.model"
    model = Word2Vec.load(model_path)
    print(f"Model loaded from {model_path}")
    # Load the graph from pickle
    graph_path = "../../models/village_graph.pkl"
    with open(graph_path, "rb") as f:
        G = pickle.load(f)
    print(f"Graph loaded from {graph_path}")
    return G, model


def _calc_similarities(G, model, svd, user_choices_cmun):

    # 2. Get all village vectors (handling missing nodes)
    all_village_vectors = {}
    for v in G.nodes():
        try:
            all_village_vectors[v] = model.wv[str(v)]
        except KeyError:
            print(f"Warning: Village {v} not found in model")
            continue
    # 3. Apply TruncatedSVD to reduce dimensionality
    all_vectors = np.array(list(all_village_vectors.values()))
    pueblos_latent_features = svd.fit_transform(all_vectors)
    # 1. Get vectors for user-selected villages
    valid_villages = []
    selected_vectors = []
    for v in user_choices_cmun:
        try:
            vector = model.wv[str(v)]
            selected_vectors.append(vector)
            valid_villages.append(v)
        except KeyError:
            print(f"Warning: Village {v} not found in model")

    user_latent_features = svd.transform(np.array(selected_vectors))
    similarities_svd = cosine_similarity(user_latent_features, pueblos_latent_features)

    df_similarities = pd.DataFrame()
    df_similarities["similarity"] = similarities_svd.mean(axis=0)

    df_similarities["cmun"] = G.nodes().keys()
    return df_similarities.sort_values(by="similarity", ascending=False)

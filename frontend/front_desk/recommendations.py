import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import uuid
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import pickle


def show():

    recommendation_selection = st.selectbox(
        "Select recommendation engine: ",
        ["SVD Sparse Matrix", "Node2Vec Graph SVD Combination"],
    )
    # Load data
    csv_path = "../../data/end_product_data/pueblos_recommender.csv"
    df_pueblos = pd.read_csv(csv_path)
    user_choices = pd.read_csv(st.session_state.output_path)

    if recommendation_selection == "SVD Sparse Matrix":
        st.write("### Your Top 5 Recommended Towns")
        st.write("Based on your preferences, here are the top recommended towns.")

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
    elif recommendation_selection == "Node2Vec Graph SVD Combination":
        user_choices_cmun = user_choices.cmun.tolist()

        svd = TruncatedSVD(n_components=5)
        model_path = "../../models/node2vec.model"
        model = Word2Vec.load(model_path)

        print(f"Model loaded from {model_path}")

        # Load the graph from pickle
        graph_path = "../../models/village_graph.pkl"
        with open(graph_path, "rb") as f:
            G = pickle.load(f)

        print(f"Graph loaded from {graph_path}")

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
        user_selected_villages = user_choices_cmun
        valid_villages = []
        selected_vectors = []

        for v in user_selected_villages:
            try:
                vector = model.wv[str(v)]
                selected_vectors.append(vector)
                valid_villages.append(v)
            except KeyError:
                print(f"Warning: Village {v} not found in model")

        user_latent_features = svd.transform(np.array(selected_vectors))

        similarities_svd = cosine_similarity(
            user_latent_features, pueblos_latent_features
        )

        df_similarities = pd.DataFrame()
        df_similarities["similarity"] = similarities_svd.mean(axis=0)

        df_similarities["cmun"] = G.nodes().keys()
        df_similarities = df_similarities.sort_values(by="similarity", ascending=False)

        st.dataframe(df_similarities)

        # Convert df_similarities to the ranked_villages format that ndcg_at_k expects
        ranked_villages_from_df = list(
            zip(df_similarities["cmun"], df_similarities["similarity"])
        )

        # Calculate NDCG score for the recommendations
        def ndcg_at_k(ranked_list, ideal_list, k):
            def dcg(scores):
                return sum([(2**s - 1) / np.log2(i + 2) for i, s in enumerate(scores)])

            ideal_scores = [1 if v in ideal_list else 0 for v, _ in ranked_list[:k]]
            return dcg(ideal_scores) / dcg(sorted(ideal_scores, reverse=True))

        # Calculate NDCG at 10
        ndcg_score = ndcg_at_k(ranked_villages_from_df, user_choices_cmun, k=10)
        print(f"NDCG Score: {ndcg_score:.4f}")

        # Display top similar villages
        print("Top 10 Most Similar Villages:")
        for village, score in ranked_villages_from_df[:10]:
            print(f"Village {village}: Similarity {score:.4f}")

        # Optional: Add village names if available
        if "municipality" in df_pueblos.columns:
            # Create a lookup dictionary for village names
            cmun_to_name = dict(zip(df_pueblos["cmun"], df_pueblos["municipality"]))

            print("\nTop 10 Most Similar Villages with Names:")
            for village, score in ranked_villages_from_df[:10]:
                village_name = cmun_to_name.get(village, "Unknown")
                print(f"Village {village} ({village_name}): Similarity {score:.4f}")

        # Visualize top similarities with a bar chart
        top_n = 10
        village_ids = [str(v) for v, _ in ranked_villages_from_df[:top_n]]
        similarity_scores = [score for _, score in ranked_villages_from_df[:top_n]]

        st.write("### Top 10 Most Similar Villages")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(
            x=village_ids,
            y=similarity_scores,
            hue=village_ids,
            palette="viridis",
            ax=ax,
            dodge=False,
        )
        ax.set_title("Top Similar Villages")
        ax.set_xlabel("Village ID")
        ax.set_ylabel("Cosine Similarity")
        ax.set_xticks(range(len(village_ids)))
        ax.set_xticklabels(village_ids, rotation=45)
        st.pyplot(fig)

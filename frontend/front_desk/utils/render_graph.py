from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import streamlit as st
import numpy as np
import pandas as pd
import pickle


def render_graph(user_choices, df_pueblos):
    svd = TruncatedSVD(n_components=5)
    user_choices_cmun = user_choices.cmun.tolist()
    G, model = load_graph_model()

    df_similarities = calc_similarities(G, model, svd, user_choices_cmun)
    st.dataframe(df_similarities)

    # Convert df_similarities to the ranked_villages format that ndcg_at_k expects
    rank_villages(df_pueblos, df_similarities)


def rank_villages(df_pueblos, df_similarities):
    ranked_villages_from_df = list(
        zip(df_similarities["cmun"], df_similarities["similarity"])
    )

    # Optional: Add village names if available
    if "municipality" in df_pueblos.columns:
        # Create a lookup dictionary for village names
        cmun_to_name = dict(zip(df_pueblos["cmun"], df_pueblos["municipality"]))

        st.write("\nTop 10 Most Similar Villages with Names:")
        for village, score in ranked_villages_from_df[:5]:
            village_name = cmun_to_name.get(village, "Unknown")
            st.write(f"Village {village} ({village_name}): Similarity {score:.4f}")


def load_graph_model():
    model_path = "../../models/node2vec.model"
    model = Word2Vec.load(model_path)
    print(f"Model loaded from {model_path}")
    # Load the graph from pickle
    graph_path = "../../models/village_graph.pkl"
    with open(graph_path, "rb") as f:
        G = pickle.load(f)
    print(f"Graph loaded from {graph_path}")
    return G, model


def calc_similarities(G, model, svd, user_choices_cmun):

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

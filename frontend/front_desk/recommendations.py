import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import uuid
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

def show():
    # CSV file path for input and output
    st.write("## Awesome! here are our recommendations for you 🏆")

    csv_path = "../../data/end-product-data/pueblos_recommender.csv"
    df_pueblos = pd.read_csv(csv_path)
    user_choices = pd.read_csv(st.session_state.output_path)
    #user_choices = pd.read_csv("../../data/user_output/user_selection_recommender_beta.csv")
    

    sparse_matrix = user_choices.filter(regex=r'^enc_', axis=1).values

    svd = TruncatedSVD(n_components=4)
    user_latent_features = svd.fit_transform(sparse_matrix)

    # Transform town data into the same latent space
    pueblos_latent_features = svd.transform(df_pueblos.filter(regex=r'^enc_', axis=1).values)

    # Compute similarities
    similarities = cosine_similarity(user_latent_features, pueblos_latent_features)

    # Get top recommended towns
    df_pueblos['similarity'] = similarities.mean(axis=0)
    df_towns = df_pueblos.sort_values(by='similarity', ascending=False)


    # Show recommendations

    st.dataframe(df_pueblos.sort_values("similarity", ascending=False).head(5))

import streamlit as st
import pandas as pd
from utils.render_svd_sparse import *
from utils.render_graph import *


def show():
    recommendation_selection = st.selectbox(
        "Select recommendation engine: ",
        ["Node2Vec Graph SVD Combination", "SVD Sparse Matrix"],
    )

    st.write("### Your Top 5 Recommended Towns")
    st.write("Based on your preferences, here are the top recommended towns.")

    # Load data
    csv_path = "../../data/end_product_data/pueblos_recommender.csv"
    df_pueblos = pd.read_csv(csv_path)
    user_choices = pd.read_csv(st.session_state.output_path)

    if recommendation_selection == "Node2Vec Graph SVD Combination":
        render_graph(user_choices, df_pueblos)

    if recommendation_selection == "SVD Sparse Matrix":
        render_svd_sparse(user_choices, df_pueblos)

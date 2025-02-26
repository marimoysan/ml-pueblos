import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import streamlit as st
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA


default_session_state = {
    "df_select": pd.DataFrame(),
    "df_cat_columns": pd.DataFrame(),
    "df_train": pd.DataFrame(),
    "df_origin": pd.DataFrame(),
    "initial_run": False,
}
# Initialize session state
for key, value in default_session_state.items():
    if key not in st.session_state:
        st.session_state[key] = value


st.set_page_config(page_title="Clustering", page_icon="✣")
st.sidebar.header("Clustering")

number_of_components = st.sidebar.slider(
    "PCA components: ", min_value=1, max_value=10, value=7, step=1
)

number_of_clusters = st.sidebar.slider(
    "Clusters: ", min_value=1, max_value=10, value=7, step=1
)


st.title("Clustering")
st.write(f"Shape: {st.session_state.df_train.shape}")

# Initialize PCA
pca = PCA(n_components=number_of_components)

# Apply PCA
pca_result = pca.fit_transform(st.session_state.df_train)

# Create a DataFrame with PCA results
pca_columns = list(f"PC{i + 1}" for i in range(number_of_components))
pca_df = pd.DataFrame(pca_result, columns=pca_columns)

# Check explained variance
st.write(
    "Explained variance ratio:",
    ", ".join(map(lambda x: f"{x:.2f}", pca.explained_variance_ratio_)),
)
total_explained_variance = pca.explained_variance_ratio_.sum()
st.write("Total explained variance ratio:", total_explained_variance)


# Initialize KMeans with desired number of clusters (e.g., 3)
agg_cluster = AgglomerativeClustering(n_clusters=number_of_clusters, linkage="ward")
agg_cluster.fit_predict(st.session_state.df_train)

# Get cluster labels
pca_df["cluster_agg"] = agg_cluster.labels_

fig = plt.figure(figsize=(8, 6))
sns.scatterplot(x="PC1", y="PC2", hue="cluster_agg", data=pca_df, palette="Set2", s=60)
plt.title("Agg Clustering on PCA-Reduced Data", fontsize=16)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()
st.pyplot(fig)


st.write(f"New shape:")
st.write(pca_df.shape)
st.dataframe(pca_df)


st.write(f"New shape:")
st.write(st.session_state["df_origin"].shape)
st.dataframe(st.session_state["df_origin"])

df_final = pd.concat([pca_df, st.session_state["df_origin"]], axis=1)
df_final.to_csv("../../data/end-product-data/pueblos_recommender.csv")

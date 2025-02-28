import pandas as pd
import streamlit as st
import datetime
from session_state_manager import initialize_session_state
from clustering_utils import (
    perform_pca,
    perform_clustering,
    create_cluster_scatter_plot,
    create_cluster_pairplot,
)

# Setup page
st.set_page_config(page_title="Clustering", page_icon="✣")
st.sidebar.header("Clustering")

# Initialize state
initialize_session_state()
st.session_state["initial_run"] = False

# Sidebar controls
number_of_components = st.sidebar.slider(
    "PCA components: ", min_value=2, max_value=10, value=4, step=1
)

number_of_clusters = st.sidebar.slider(
    "Clusters: ", min_value=2, max_value=10, value=4, step=1
)

clustering_method = st.sidebar.selectbox(
    "Clustering Method", ["Agglomerative", "KMeans", "DBSCAN"], index=0
)

st.title("Clustering")
st.write(f"Shape: {st.session_state.df_train.shape}")

# Perform PCA
pca_df, pca_model, explained_variance = perform_pca(
    st.session_state.df_train, number_of_components
)

# Display PCA information
st.write("Explained variance ratio:", ", ".join(f"{x:.2f}" for x in explained_variance))
st.write("Total explained variance ratio:", explained_variance.sum())

# Perform clustering
cluster_labels, cluster_model = perform_clustering(
    st.session_state.df_train,
    method=clustering_method.lower(),
    n_clusters=number_of_clusters,
)

# Add cluster labels to PCA dataframe
pca_df["cluster"] = cluster_labels

# Create and display the plot
cluster_plot = create_cluster_scatter_plot(
    pca_df, cluster_labels, f"{clustering_method} Clustering on PCA-Reduced Data"
)
st.pyplot(cluster_plot)


st.write("---")
pairplot = create_cluster_pairplot(pca_df, cluster_labels)
st.pyplot(pairplot)

st.write("---")


# Display dataframes
st.write(f"PCA DataFrame Shape: {pca_df.shape}")
st.dataframe(pca_df)

st.write(f"Original DataFrame Shape: {st.session_state['df_origin'].shape}")
st.dataframe(st.session_state["df_origin"])

# Combine dataframes
pca_df.reset_index(drop=True, inplace=True)
st.session_state["df_origin"].reset_index(drop=True, inplace=True)

df_final = pd.concat(
    [st.session_state["df_origin"], pca_df, st.session_state["df_train"]], axis=1
)

st.write("Combined DataFrame")
st.dataframe(df_final)

# Save option
if st.button("Save DataFrame to CSV"):
    timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    filename = f"../../data/interim/pueblos_recommender_{timestamp}.csv"
    df_final.to_csv(filename, index=False)
    st.write(f"DataFrame saved to {filename}")

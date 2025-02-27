import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
import matplotlib.pyplot as plt
import seaborn as sns


def perform_pca(data, n_components):
    """
    Performs PCA dimensionality reduction

    Parameters:
    -----------
    data : pandas.DataFrame
        The input data for PCA
    n_components : int
        Number of PCA components to extract

    Returns:
    --------
    tuple
        (pca_df, pca_model, explained_variance_ratio)
    """
    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(data)
    pca_columns = [f"PC{i + 1}" for i in range(n_components)]
    pca_df = pd.DataFrame(pca_result, columns=pca_columns)

    return pca_df, pca, pca.explained_variance_ratio_


def perform_clustering(data, method="agglomerative", n_clusters=4, **kwargs):
    """
    Performs clustering on the input data

    Parameters:
    -----------
    data : pandas.DataFrame
        The input data for clustering
    method : str
        Clustering method: 'agglomerative', 'kmeans', or 'dbscan'
    n_clusters : int
        Number of clusters (for agglomerative and kmeans)
    **kwargs : dict
        Additional parameters for the clustering algorithm

    Returns:
    --------
    tuple
        (labels, model)
    """
    if method.lower() == "agglomerative":
        model = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward", **kwargs)
    elif method.lower() == "kmeans":
        model = KMeans(n_clusters=n_clusters, random_state=42, **kwargs)
    elif method.lower() == "dbscan":
        model = DBSCAN(**kwargs)
    else:
        raise ValueError("Method must be one of: 'agglomerative', 'kmeans', 'dbscan'")

    labels = model.fit_predict(data)
    return labels, model


def create_cluster_scatter_plot(pca_df, labels, title="Clustering on PCA-Reduced Data"):
    """
    Creates a scatter plot of clusters on the first two PCA components

    Parameters:
    -----------
    pca_df : pandas.DataFrame
        DataFrame containing PCA components
    labels : array-like
        Cluster labels
    title : str
        Plot title

    Returns:
    --------
    matplotlib.figure.Figure
        The scatter plot figure
    """
    fig = plt.figure(figsize=(8, 6))
    pca_with_clusters = pca_df.copy()
    pca_with_clusters["cluster"] = labels

    sns.scatterplot(
        x="PC1", y="PC2", hue="cluster", data=pca_with_clusters, palette="Set2", s=60
    )
    plt.title(title, fontsize=16)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend()

    return fig



import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def create_cluster_pairplot(pca_df, labels, title="Pairplot of Clusters on PCA-Reduced Data"):
    """
    Creates a Seaborn pairplot of clusters on multiple PCA components.

    Parameters:
    -----------
    pca_df : pandas.DataFrame
        DataFrame containing PCA components.
    labels : array-like
        Cluster labels.
    title : str
        Title for the plot.

    Returns:
    --------
    seaborn.axisgrid.PairGrid
        The pairplot figure.
    """
    pca_with_clusters = pca_df.copy()
    pca_with_clusters["cluster"] = labels  # Add cluster labels

    # Create pairplot with hue as clusters
    pairplot = sns.pairplot(pca_with_clusters, hue="cluster", palette="Set2", diag_kind="hist")

    # Set title
    pairplot.fig.suptitle(title, fontsize=16, y=1.02)

    return pairplot




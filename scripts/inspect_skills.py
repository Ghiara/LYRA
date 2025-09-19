import chromadb
from agents.model import Skill
from agents.memory import SkillManager, MemoryManager
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

import mplcursors


def get_ids_and_embeddings():
    memory_manager = MemoryManager()
    skill_manager = memory_manager.skill_manager
    ids, embeddings = skill_manager.get_all_skill_embeddings()
    return ids, embeddings


def plot_elbow_curve(embeddings):
    pca = PCA(n_components=5)
    pca_embeddings = pca.fit_transform(embeddings)

    wcss = []  # Within-cluster sum of squares
    for k in range(1, 20):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(pca_embeddings)
        wcss.append(kmeans.inertia_)

    plt.plot(range(1, 20), wcss, marker="o")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("WCSS")
    plt.title("Elbow Method for Optimal k")
    plt.show()


def cluster_embeddings(ids, embeddings, num_clusters):
    tsne = TSNE(n_components=2, perplexity=10, random_state=42)
    tsne_embeddings = tsne.fit_transform(embeddings)

    pca = PCA(n_components=5)
    pca_embeddings = pca.fit_transform(embeddings)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(tsne_embeddings)

    sc = plt.scatter(
        tsne_embeddings[:, 0],
        tsne_embeddings[:, 1],
        c=labels,
        cmap="viridis",
        alpha=0.6,
    )

    centers = kmeans.cluster_centers_
    plt.scatter(
        centers[:, 0],
        centers[:, 1],
        c="red",
        marker="X",
        s=100,
        label="Cluster Centers",
    )

    cursor = mplcursors.cursor(sc, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"{ids[sel.index]}"))

    plt.title("K-Means Clustering")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    ids, embeddings = get_ids_and_embeddings()
    # plot_elbow_curve(embeddings)
    cluster_embeddings(ids, embeddings, 10)

import pandas as pd
import numpy as np
import os
import pickle

# imports
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # points to 'backend' folder
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(DATA_PATH, exist_ok=True)

# 1. load data
print("---Loading Data ---")


raw_data = [
    # tech cluster
    "Artificial Intelligence is transforming healthcare rapidly.",
    "The new iPhone features a titanium frame and better battery.",
    "Nvidia stocks rose after the GPU announcement.",
    "Python is the most popular language for Data Science.",
    "Quantum computing will break current encryption methods.",
    
    # sports cluster
    "The Lakers won the game with a last-minute buzzer beater.",
    "Lionel Messi scored a hat-trick in the final match.",
    "The Olympic games will be held in Paris next year.",
    "Tennis star announces retirement after 20 years.",
    "Formula 1 introduces new regulations for car aerodynamics.",
    
    # finance cluster
    "The Federal Reserve decided to keep interest rates unchanged.",
    "Inflation creates pressure on global supply chains.",
    "Bitcoin dropped 5% following the regulatory news.",
    "Wall Street analysts predict a recession next quarter.",
    "The housing market is slowing down due to high mortgages."
]

# create dataframe
df = pd.DataFrame(raw_data, columns=['text'])
df['clean_text'] = df['text'].str.lower()
print(f"Loaded {len(df)} documents.")


# 2. embbegings (PyTorch)
print("\n--- Generating Embeddings (PyTorch) ---")
# downloard the model (apper once)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# convert text to vectors
embeddings = embedder.encode(df['clean_text'].tolist())
df['vector'] = list(embeddings)
print(f"Embeddings shape: {embeddings.shape}")


# 3. clustering
print("\n--- Clustering Data ---")
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(embeddings)
df['cluster'] = kmeans.labels_

print("Clustering Results:")
print(df[['text', 'cluster']].sort_values(by='cluster'))


# 4. save & plot
print("\n--- Saving & Plotting ---")

# save for the next phase
save_file = os.path.join(DATA_PATH, "clustered_data.pkl")
df.to_pickle(save_file)
print(f"Data saved to: {save_file}")

# visualizing
pca = PCA(n_components=2)
coords = pca.fit_transform(embeddings)

plt.figure(figsize=(10, 6))
colors = ['red', 'blue', 'green']

for cluster_id in range(3):
    points = coords[df['cluster'] == cluster_id]
    plt.scatter(points[:, 0], points[:, 1], c=colors[cluster_id], label=f"Cluster {cluster_id}")

plt.title("AI Perception of Data")
plt.legend()
plt.grid(True)
plt.show()
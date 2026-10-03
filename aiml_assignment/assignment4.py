import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# --- 1. Synthetic Telemetry Generator ---
def generate_network_traffic_dataset(n_samples: int = 1500, random_seed: int = 42) -> pd.DataFrame:
    np.random.seed(random_seed)
    counts = [500, 350, 350, 300]

    # Profile 0: Interactive Web/Admin
    f1_c0 = np.random.normal(loc=12000.0, scale=3000.0, size=counts[0])
    f2_c0 = np.random.normal(loc=150.0, scale=35.0, size=counts[0])
    f3_c0 = np.random.normal(loc=85.0, scale=18.0, size=counts[0])
    f4_c0 = np.random.normal(loc=7.10, scale=0.35, size=counts[0])

    # Profile 1: High-Volume Bulk Transfer / Exfiltration
    f1_c1 = np.random.normal(loc=65000.0, scale=12000.0, size=counts[1])
    f2_c1 = np.random.normal(loc=2400.0, scale=350.0, size=counts[1])
    f3_c1 = np.random.normal(loc=12.0, scale=3.5, size=counts[1])
    f4_c1 = np.random.normal(loc=7.75, scale=0.15, size=counts[1])

    # Profile 2: Stealth Reconnaissance Scan
    f1_c2 = np.random.normal(loc=35000.0, scale=8000.0, size=counts[2])
    f2_c2 = np.random.normal(loc=18.0, scale=5.0, size=counts[2])
    f3_c2 = np.random.normal(loc=450.0, scale=75.0, size=counts[2])
    f4_c2 = np.random.normal(loc=1.80, scale=0.40, size=counts[2])

    # Profile 3: Volumetric DoS Flood
    f1_c3 = np.random.normal(loc=2500.0, scale=600.0, size=counts[3])
    f2_c3 = np.random.normal(loc=1200.0, scale=200.0, size=counts[3])
    f3_c3 = np.random.normal(loc=2.1, scale=0.6, size=counts[3])
    f4_c3 = np.random.normal(loc=3.20, scale=0.50, size=counts[3])

    flow_duration = np.clip(np.concatenate([f1_c0, f1_c1, f1_c2, f1_c3]), 100.0, 120000.0)
    packet_count = np.clip(np.concatenate([f2_c0, f2_c1, f2_c2, f2_c3]), 2.0, 5000.0)
    mean_iat = np.clip(np.concatenate([f3_c0, f3_c1, f3_c2, f3_c3]), 0.5, 1000.0)
    entropy = np.clip(np.concatenate([f4_c0, f4_c1, f4_c2, f4_c3]), 0.05, 7.99)

    df = pd.DataFrame({
        "Flow_Duration_ms": np.round(flow_duration, 2),
        "Total_Packets": np.round(packet_count, 0).astype(int),
        "Mean_IAT_ms": np.round(mean_iat, 2),
        "Payload_Entropy": np.round(entropy, 3)
    })

    shuffled_indices = np.random.permutation(len(df))
    return df.iloc[shuffled_indices].reset_index(drop=True)


# --- 2. Custom K-Means Implementation ---
class CustomKMeans:
    def __init__(self, n_clusters: int = 4, max_iter: int = 300, tol: float = 1e-4, random_state: int = 42):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None

    def fit(self, X: np.ndarray, init_centroids: np.ndarray = None):
        np.random.seed(self.random_state)
        n_samples, n_features = X.shape

        if init_centroids is not None:
            self.cluster_centers_ = init_centroids.copy()
        else:
            random_idx = np.random.choice(n_samples, self.n_clusters, replace=False)
            self.cluster_centers_ = X[random_idx]

        for i in range(self.max_iter):
            # Expectation Step: Distance Matrix Computation using Euclidean distance formula
            # ||X - C||^2 = ||X||^2 + ||C||^2 - 2 * X * C^T
            distances = np.linalg.norm(X[:, np.newaxis] - self.cluster_centers_, axis=2)
            self.labels_ = np.argmin(distances, axis=1)

            # Maximization Step: Centroid recalculation
            new_centroids = np.array([
                X[self.labels_ == k].mean(axis=0) if np.sum(self.labels_ == k) > 0 else self.cluster_centers_[k]
                for k in range(self.n_clusters)
            ])

            # Check convergence
            center_shift = np.sum((self.cluster_centers_ - new_centroids) ** 2)
            self.cluster_centers_ = new_centroids

            if center_shift <= self.tol:
                break

        # Calculate Within-Cluster Sum of Squares (Inertia)
        min_distances = np.min(np.linalg.norm(X[:, np.newaxis] - self.cluster_centers_, axis=2), axis=1)
        self.inertia_ = np.sum(min_distances ** 2)
        return self


# --- 3. Execution & Verification ---
if __name__ == "__main__":
    df = generate_network_traffic_dataset(n_samples=1500, random_seed=42)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df.values)

    # Initialize fixed centroids for direct comparison verification
    np.random.seed(42)
    init_idx = np.random.choice(X_scaled.shape[0], 4, replace=False)
    initial_centroids = X_scaled[init_idx]

    # Custom Implementation
    custom_kmeans = CustomKMeans(n_clusters=4, max_iter=300, random_state=42)
    custom_kmeans.fit(X_scaled, init_centroids=initial_centroids)

    # Scikit-Learn Benchmark
    sklearn_kmeans = KMeans(n_clusters=4, init=initial_centroids, n_init=1, max_iter=300, random_state=42)
    sklearn_kmeans.fit(X_scaled)

    # Sort centroids for aligned 1-to-1 comparison
    custom_order = np.argsort(custom_kmeans.cluster_centers_[:, 0])
    sklearn_order = np.argsort(sklearn_kmeans.cluster_centers_[:, 0])

    c_custom = custom_kmeans.cluster_centers_[custom_order]
    c_sklearn = sklearn_kmeans.cluster_centers_[sklearn_order]

    print("--- Centroid Verification (Scaled Space) ---")
    print(f"{'Cluster':<8} | {'Custom Centroid (First 2 Features)':<35} | {'Sklearn Centroid (First 2 Features)':<35}")
    print("-" * 85)
    for k in range(4):
        c_str = np.array2string(c_custom[k][:2], precision=4)
        sk_str = np.array2string(c_sklearn[k][:2], precision=4)
        print(f"{k:<8} | {c_str:<35} | {sk_str:<35}")

    print("\n--- Final Metrics Comparison ---")
    print(f"Custom Inertia:  {custom_kmeans.inertia_:.4f}")
    print(f"Sklearn Inertia: {sklearn_kmeans.inertia_:.4f}")

    centroids_match = np.allclose(c_custom, c_sklearn, atol=1e-4)
    inertia_match = np.isclose(custom_kmeans.inertia_, sklearn_kmeans.inertia_, atol=1e-4)

    print(f"\nCentroids Match: {centroids_match}")
    print(f"Inertia Matches:   {inertia_match}")
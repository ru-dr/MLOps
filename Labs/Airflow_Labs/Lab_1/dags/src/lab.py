import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from kneed import KneeLocator
import pickle
import os
import base64
import json

FEATURES = ["BALANCE", "PURCHASES", "CREDIT_LIMIT"]
K_RANGE = range(1, 50)
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")


def load_data():
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.
    Returns:
        str: Base64-encoded serialized data (JSON-safe).
    """
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
    print(f"Loaded {len(df)} rows, {df.shape[1]} columns")
    serialized_data = pickle.dumps(df)                    # bytes
    return base64.b64encode(serialized_data).decode("ascii")  # JSON-safe string


def data_preprocessing(data_b64: str):
    """
    Deserializes base64-encoded pickled data, drops missing rows, min-max scales
    the clustering features, saves the fitted scaler next to the model, and
    returns the scaled data as a base64-encoded pickle.
    """
    df = pickle.loads(base64.b64decode(data_b64))

    df = df.dropna()
    clustering_data = df[FEATURES]

    min_max_scaler = MinMaxScaler()
    clustering_data_minmax = min_max_scaler.fit_transform(clustering_data)

    # keep the scaler so new data can be scaled the same way at prediction time
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(os.path.join(MODEL_DIR, "scaler.sav"), "wb") as f:
        pickle.dump(min_max_scaler, f)

    clustering_serialized_data = pickle.dumps(clustering_data_minmax)
    return base64.b64encode(clustering_serialized_data).decode("ascii")


def build_save_model(data_b64: str, filename: str):
    """
    Sweeps k over K_RANGE, picks k with the elbow method, refits KMeans at that k,
    saves it, and returns the SSE list plus the chosen k and its silhouette score.
    """
    data = pickle.loads(base64.b64decode(data_b64))

    kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42}
    sse = []
    for k in K_RANGE:
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(data)
        sse.append(kmeans.inertia_)

    kl = KneeLocator(list(K_RANGE), sse, curve="convex", direction="decreasing")
    best_k = int(kl.elbow) if kl.elbow else 3  # fall back to a sane default
    print(f"Elbow k = {best_k}")

    best_model = KMeans(n_clusters=best_k, **kmeans_kwargs).fit(data)
    silhouette = float(silhouette_score(data, best_model.labels_))
    print(f"Silhouette score at k={best_k}: {silhouette:.4f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(os.path.join(MODEL_DIR, filename), "wb") as f:
        pickle.dump(best_model, f)

    return {"sse": sse, "best_k": best_k, "silhouette": silhouette}  # JSON-safe


def load_model_elbow(filename: str, summary: dict):
    """
    Loads the saved model and scaler, scales test.csv with the training scaler,
    and returns the predicted cluster of the first test row as a plain int.
    """
    with open(os.path.join(MODEL_DIR, filename), "rb") as f:
        loaded_model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, "scaler.sav"), "rb") as f:
        scaler = pickle.load(f)

    print(f"Optimal no. of clusters: {summary['best_k']} (silhouette {summary['silhouette']:.4f})")

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test.csv"))
    pred = loaded_model.predict(scaler.transform(df[FEATURES]))[0]
    print(f"Test row assigned to cluster {int(pred)}")

    return int(pred)


def save_cluster_report(filename: str, summary: dict):
    """
    Profiles the saved model: cluster sizes and centroids in original units.
    Writes model/cluster_report.json and returns the cluster sizes (JSON-safe).
    """
    with open(os.path.join(MODEL_DIR, filename), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, "scaler.sav"), "rb") as f:
        scaler = pickle.load(f)

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv")).dropna()
    labels = model.predict(scaler.transform(df[FEATURES]))
    sizes = {int(c): int(n) for c, n in pd.Series(labels).value_counts().sort_index().items()}

    centroids = pd.DataFrame(scaler.inverse_transform(model.cluster_centers_), columns=FEATURES).round(2)
    report = {
        "best_k": summary["best_k"],
        "silhouette": summary["silhouette"],
        "cluster_sizes": sizes,
        "centroids": centroids.to_dict(orient="index"),
    }
    with open(os.path.join(MODEL_DIR, "cluster_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    print(f"Cluster sizes: {sizes}")
    return sizes

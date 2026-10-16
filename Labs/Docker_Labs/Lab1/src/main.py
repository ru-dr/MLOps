import json
import os
from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


def load_config():
    return {
        "n_estimators": int(os.getenv("N_ESTIMATORS", "100")),
        "test_size": float(os.getenv("TEST_SIZE", "0.2")),
        "random_state": int(os.getenv("RANDOM_STATE", "42")),
        "min_accuracy": float(os.getenv("MIN_ACCURACY", "0.85")),
        "output_dir": os.getenv("OUTPUT_DIR", "output"),
    }


def train(n_estimators, test_size, random_state):
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=test_size, random_state=random_state, stratify=iris.target
    )
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)
    return model, X_test, y_test, iris.target_names


def evaluate(model, X_test, y_test, target_names):
    predictions = model.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, predictions),
        "report": classification_report(y_test, predictions, target_names=target_names, output_dict=True),
    }


def save(model, metrics, config, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "iris_model.pkl"
    metrics_path = output_dir / "metrics.json"
    joblib.dump(model, model_path)
    metrics_path.write_text(json.dumps({"config": config, **metrics}, indent=2))
    return model_path, metrics_path


def run(config):
    model, X_test, y_test, target_names = train(config["n_estimators"], config["test_size"], config["random_state"])
    metrics = evaluate(model, X_test, y_test, target_names)
    if metrics["accuracy"] < config["min_accuracy"]:
        raise SystemExit(f"Accuracy {metrics['accuracy']:.3f} is below the minimum {config['min_accuracy']}")
    model_path, metrics_path = save(model, metrics, config, config["output_dir"])
    return metrics, model_path, metrics_path


if __name__ == '__main__':
    metrics, model_path, metrics_path = run(load_config())
    print(f"Test accuracy: {metrics['accuracy']:.3f}")
    print(f"Model saved to {model_path}, metrics saved to {metrics_path}")
    print("The model training was successful")

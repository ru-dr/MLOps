import json
import sys
from pathlib import Path

import joblib
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import main


def test_load_config_defaults(monkeypatch):
    for var in ("N_ESTIMATORS", "TEST_SIZE", "RANDOM_STATE", "MIN_ACCURACY", "OUTPUT_DIR"):
        monkeypatch.delenv(var, raising=False)
    assert main.load_config() == {
        "n_estimators": 100,
        "test_size": 0.2,
        "random_state": 42,
        "min_accuracy": 0.85,
        "output_dir": "output",
    }


def test_load_config_reads_env(monkeypatch):
    monkeypatch.setenv("N_ESTIMATORS", "10")
    monkeypatch.setenv("TEST_SIZE", "0.3")
    config = main.load_config()
    assert config["n_estimators"] == 10
    assert config["test_size"] == 0.3


def test_train_split_sizes():
    model, X_test, y_test, target_names = main.train(n_estimators=10, test_size=0.2, random_state=0)
    assert len(X_test) == len(y_test) == 30
    assert list(target_names) == ["setosa", "versicolor", "virginica"]
    assert model.n_estimators == 10


def test_evaluate_accuracy_is_high():
    model, X_test, y_test, target_names = main.train(n_estimators=50, test_size=0.2, random_state=42)
    metrics = main.evaluate(model, X_test, y_test, target_names)
    assert metrics["accuracy"] >= 0.9
    assert set(target_names) <= metrics["report"].keys()


def test_run_writes_artifacts(tmp_path):
    config = {**main.load_config(), "output_dir": str(tmp_path)}
    metrics, model_path, metrics_path = main.run(config)
    loaded = joblib.load(model_path)
    assert loaded.predict([[5.1, 3.5, 1.4, 0.2]])[0] == 0
    saved = json.loads(metrics_path.read_text())
    assert saved["accuracy"] == metrics["accuracy"]
    assert saved["config"]["output_dir"] == str(tmp_path)


def test_run_fails_below_min_accuracy(tmp_path):
    config = {**main.load_config(), "output_dir": str(tmp_path), "min_accuracy": 1.01}
    with pytest.raises(SystemExit, match="below the minimum"):
        main.run(config)
    assert not (tmp_path / "iris_model.pkl").exists()

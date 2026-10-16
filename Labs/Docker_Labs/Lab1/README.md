# Docker Lab 1: Containerized Iris Training

Trains a Random Forest on the Iris dataset inside a container, evaluates it on a held-out split,
and writes the model plus a `metrics.json` file to `/app/output`.

## Changes from the original lab
- `src/main.py` refactored into `load_config`, `train`, `evaluate`, `save` and `run` functions
- Train/test split is stratified so every class is represented in the test set
- Model and `metrics.json` are written to `/app/output` and can be kept on the host with a volume mount
- `tests/test_main.py` adds a pytest suite covering config, training, evaluation, saved artifacts and the accuracy gate
- `python:3.12-slim` base image with pinned dependencies and a cached pip layer
- Multi-stage `dockerfile`: `test` stage runs pytest, `train` stage runs as a non-root user
- Training reports test accuracy and a per-class report, and exits non-zero if accuracy is below `MIN_ACCURACY`
- Training settings configurable through environment variables
- `.dockerignore` keeps caches and artifacts out of the build context

## Usage
```bash
# Run the tests inside a container
docker build --target test -t lab1:test .

# Build the training image
docker build -t lab1:v1 .

# Train and keep the artifacts on the host
docker run --rm -v "$(pwd)/output:/app/output" lab1:v1

# Override settings
docker run --rm -e N_ESTIMATORS=200 -e TEST_SIZE=0.3 -v "$(pwd)/output:/app/output" lab1:v1

# Save the image to a tarball
docker save lab1:v1 > my_image.tar
```

## Configuration
| Variable | Default | Description |
|---|---|---|
| `N_ESTIMATORS` | `100` | Number of trees |
| `TEST_SIZE` | `0.2` | Fraction of data held out for testing |
| `RANDOM_STATE` | `42` | Seed for the split and the model |
| `MIN_ACCURACY` | `0.85` | Training fails below this test accuracy |
| `OUTPUT_DIR` | `output` | Where the model and metrics are written |

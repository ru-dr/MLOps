# Lab 1 – DADS 7305: MLOps

Based on the course lab: [raminmohammadi/MLOps – Labs/Github_Labs/Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Github_Labs/Lab1)

Calculator module with pytest + unittest suites, run on every push/PR to `main` via GitHub Actions.

## Structure
```
data/                      # datasets (placeholder)
src/calculator.py          # calculator functions
test/test_pytest.py        # pytest suite (parametrized + error cases)
test/test_unittest.py      # unittest suite (assertRaises + subTest)
workflows/                 # pytest_action.yml, unittest_action.yml
```

## Calculator functions
| Function | Description |
|---|---|
| `fun1(x, y)` | x + y |
| `fun2(x, y)` | x - y |
| `fun3(x, y)` | x * y |
| `fun4(x, y, z)` | x + y + z |
| `divide(x, y)` | x / y, raises `ZeroDivisionError` when y is 0 |
| `power(base, exponent)` | base ** exponent, rejects complex results and 0 to a negative power |
| `square_root(x)` | √x, raises `ValueError` for negative x |
| `mean(values)` | arithmetic mean, raises `ValueError` for an empty sequence |

Every function raises `ValueError` for non-numeric input (booleans included).

## Additions beyond the reference lab
- New functions: `divide`, `power`, `square_root`, `mean`, plus shared input validation (`fun4` now validates too).
- Tests: `pytest.mark.parametrize`, `pytest.raises` / `assertRaises`, `subTest` for invalid-input cases.
- CI:
  - Latest actions: `checkout@v7`, `setup-python@v7`, `upload-artifact@v7`
  - Python matrix 3.11–3.14
  - pip caching
  - Coverage via `pytest-cov` with a 90% minimum, summary in the job page, reports uploaded as artifacts
  - `concurrency` cancels outdated runs
  - Read-only `permissions`
  - Manual runs via `workflow_dispatch`

## Run locally
```
python -m venv lab_01
source lab_01/bin/activate      # Windows: lab_01\Scripts\activate
pip install -r requirements.txt
pytest --cov=src --cov-report=term-missing
python -m unittest test.test_unittest -v
```

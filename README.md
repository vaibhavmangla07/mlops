# Batch Signal Pipeline

A lightweight, reproducible, Dockerized batch processing pipeline that reads OHLCV market data, computes a rolling mean on the `close` column, generates a binary trading signal, and outputs structured metrics with detailed logging.

Built with engineering quality in mind — clean architecture, proper validation, deterministic execution, and production-grade observability.

---

## Features

- **Configurable** — YAML-driven pipeline parameters (seed, window, version)
- **Validated** — Input data and configuration are validated before processing
- **Deterministic** — Same input + same seed = same output, every time
- **Observable** — Structured JSON metrics and timestamped log files
- **Containerized** — Docker support with single-command build and run
- **Modular** — Clean separation of concerns across focused modules

---

## Folder Structure

```
Batch-Signal-Pipeline/
├── run.py              # Entry point — orchestrates the full pipeline
├── config.yaml         # Pipeline configuration (seed, window, version)
├── data.csv            # Input OHLCV dataset (10,000 rows)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container build specification
├── metrics.json        # Sample output — pipeline metrics
├── run.log             # Sample output — execution log
├── README.md
│
└── src/
    ├── __init__.py     # Package init
    ├── constants.py    # Shared constants (keys, formats, status values)
    ├── exception.py    # Custom exceptions (Config, Data, Processing)
    ├── logger.py       # Dual-output logging setup (file + console)
    ├── config.py       # YAML loading, validation, seed initialization
    ├── validator.py    # Input file and CSV validation
    ├── processor.py    # Rolling mean + signal generation
    ├── metrics.py      # Metrics construction and persistence
    └── utils.py        # Reusable helpers (JSON writing, timing)
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/vaibhavmangla07/mlops.git
cd mlops

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `pandas` | Data loading and manipulation |
| `numpy` | Random seed for deterministic execution |
| `pyyaml` | YAML configuration parsing |

---

## Local Execution

```bash
python run.py \
  --input data.csv \
  --config config.yaml \
  --output metrics.json \
  --log-file run.log
```

### CLI Flags

| Flag | Required | Description |
|------|----------|-------------|
| `--input` | Yes | Path to input OHLCV CSV file |
| `--config` | Yes | Path to YAML configuration file |
| `--output` | Yes | Path to write metrics JSON |
| `--log-file` | Yes | Path to write execution log |

---

## Docker

### Build

```bash
docker build -t mlops-task .
```

### Run

```bash
docker run --rm mlops-task
```

The container generates `metrics.json` and `run.log` internally, prints the metrics JSON to stdout, and exits with code `0` on success or non-zero on failure.

---

## Configuration

The pipeline reads from `config.yaml`:

```yaml
seed: 42       # NumPy random seed — ensures deterministic execution
window: 5      # Rolling mean window size
version: "v1"  # Version tag included in output metrics
```

All three keys must be present. The pipeline validates their existence before processing.

---

## Example Output

### metrics.json (success)

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 29,
  "seed": 42,
  "status": "success"
}
```

### metrics.json (error)

```json
{
  "version": "unknown",
  "status": "error",
  "error_message": "Input file not found: missing.csv"
}
```

---

## Logging

The pipeline uses Python's `logging` module with dual output — file and console (stderr). Log entries are timestamped and follow this sequence:

```
2026-07-01 10:28:14,708 [INFO] Job started
2026-07-01 10:28:14,709 [INFO] Config loaded — seed=42, window=5, version=v1
2026-07-01 10:28:14,728 [INFO] Data loaded — 10000 rows
2026-07-01 10:28:14,731 [INFO] Rolling mean computed
2026-07-01 10:28:14,736 [INFO] Signal generated
2026-07-01 10:28:14,736 [INFO] Metrics — signal_rate=0.4991, rows_processed=10000, latency_ms=29
2026-07-01 10:28:14,736 [INFO] Metrics written to metrics.json
2026-07-01 10:28:14,736 [INFO] Job completed — status=success
```

Console output goes to stderr so that Docker's stdout remains clean for metrics JSON output.

---

## Error Handling

The pipeline handles failures gracefully using three custom exceptions:

| Exception | Trigger |
|-----------|---------|
| `ConfigurationError` | Missing config file, invalid YAML, missing keys |
| `DataValidationError` | Missing input file, invalid CSV, empty file, missing columns |
| `ProcessingError` | Rolling mean or signal generation failure |

On any failure:
1. The error is logged with full context
2. An error `metrics.json` is written (metrics file is **always** generated)
3. The process exits with a non-zero exit code

---

## Design Decisions

- **Modular `src/` package** — Each module has a single responsibility. `run.py` is a thin orchestrator that reads top-to-bottom.
- **Custom exceptions over generic ones** — Makes error categorization clear in logs and metrics without a complex hierarchy.
- **NaN handling** — The first `window - 1` rows produce NaN rolling means and are excluded from signal computation and metrics. This is intentional and documented.
- **Stderr for console logs** — Keeps stdout clean for Docker metrics output via `cat metrics.json`.
- **Constants module** — Eliminates magic strings. Required keys, status values, and formats are defined once.
- **No over-engineering** — No design patterns, no frameworks, no abstraction layers beyond what readability requires.

---

## Future Improvements

- Add unit tests with `pytest` for each `src/` module
- Support multiple signal strategies via config
- Add data drift detection on the `close` column
- CI/CD pipeline with GitHub Actions for automated testing and Docker builds
- Parameterized window sweep for signal optimization

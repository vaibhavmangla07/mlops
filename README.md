# MLOps Batch Job — Rolling Mean Signal Pipeline

A minimal, production-clean batch job that reads OHLCV data, computes a rolling mean on the `close` column, generates a binary trading signal, and writes structured metrics + logs.

## Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

## Docker

```bash
# Build
docker build -t mlops-task .

# Run
docker run --rm mlops-task
```

The container prints `metrics.json` to stdout and exits `0` on success / non-zero on failure.

## CLI Flags

| Flag | Required | Description |
|------|----------|-------------|
| `--input` | Yes | Path to OHLCV CSV file |
| `--config` | Yes | Path to YAML config |
| `--output` | Yes | Path to write metrics JSON |
| `--log-file` | Yes | Path to write log file |

## Config (`config.yaml`)

```yaml
seed: 42       # numpy random seed for determinism
window: 5      # rolling mean window size
version: "v1"  # version tag included in metrics
```

All three keys must be present or the job exits with an error.

## Pipeline Steps

1. Parse CLI arguments
2. Load and validate `config.yaml` (seed, window, version)
3. Set `numpy.random.seed(seed)`
4. Load and validate `data.csv` (must have a `close` column)
5. Compute rolling mean of `close` with the configured window
6. Generate binary signal: `1` if `close > rolling_mean`, else `0`
7. Write `metrics.json` and `run.log`

## Example Output

**`metrics.json`** (success):
```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 20,
  "seed": 42,
  "status": "success"
}
```

**`metrics.json`** (error):
```json
{
  "version": "v1",
  "status": "error",
  "error_message": "Input file not found: missing.csv"
}
```

## Files

| File | Purpose |
|------|---------|
| `run.py` | Main pipeline script |
| `config.yaml` | Configuration |
| `data.csv` | Input OHLCV data (10,000 rows) |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container build spec |
| `metrics.json` | Output metrics (sample committed) |
| `run.log` | Output logs (sample committed) |

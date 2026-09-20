"""
Flask server for the time complexity visualizer.

GET /analyze?algo=<name>&step=<int>&n_max=<int>
    Runs <name> on input sizes 0, step, 2*step, ... up to n_max,
    timing each run, plots the results with matplotlib, saves a PNG
    snapshot to disk, and returns the timing data plus a base64
    encoding of that same PNG.

GET /algorithms
    Lists the supported algorithm names, their Big-O complexity, and
    the safe max n for each.

Run with:  python app.py
Then try:  http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10000
"""

import base64
import io
import os
import re
import time
from datetime import datetime

import matplotlib
matplotlib.use("Agg")  # headless backend — there is no display in a server process
import matplotlib.pyplot as plt

from flask import Flask, jsonify, request

from algorithms import ALGORITHM_CONFIG

app = Flask(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snapshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Hard ceiling on how many (n, time) samples one request can generate,
# independent of n_max/step, so a request can't accidentally ask for
# thousands of runs.
MAX_DATA_POINTS = 300


def _clean_algo_name(raw: str) -> str:
    """Pull a bare algorithm name out of a possibly messy query
    param, e.g. "['linear_search'" -> "linear_search"."""
    return re.sub(r"[^a-zA-Z_]", "", raw or "").lower()


def _clean_int(raw, default: int) -> int:
    """Parse an int query param that may contain thousands
    separators or stray characters, e.g. "10,000" -> 10000."""
    if raw is None:
        return default
    cleaned = re.sub(r"[^0-9]", "", str(raw))
    return int(cleaned) if cleaned else default


@app.route("/algorithms", methods=["GET"])
def list_algorithms():
    return jsonify({
        name: {"complexity": cfg["complexity"], "max_n": cfg["max_n"]}
        for name, cfg in ALGORITHM_CONFIG.items()
    })


@app.route("/analyze", methods=["GET"])
def analyze():
    warnings = []

    # --- parse & validate algo ---
    algo_name = _clean_algo_name(request.args.get("algo", ""))
    if algo_name not in ALGORITHM_CONFIG:
        return jsonify({
            "error": f"Unknown or missing algorithm '{algo_name}'.",
            "supported_algorithms": list(ALGORITHM_CONFIG.keys()),
        }), 400

    config = ALGORITHM_CONFIG[algo_name]
    algorithm = config["func"]

    # --- parse step / n_max (n_min is always 0, per spec) ---
    step = _clean_int(request.args.get("step"), 1)
    if step <= 0:
        return jsonify({"error": "'step' must be a positive integer."}), 400

    n_min = 0
    n_max_requested = _clean_int(request.args.get("n_max"), 100)

    n_max = n_max_requested
    if n_max > config["max_n"]:
        n_max = config["max_n"]
        warnings.append(
            f"n_max clamped from {n_max_requested} to {n_max} to keep "
            f"{algo_name} ({config['complexity']}) from running too long."
        )

    # Cap the number of sample points too, independent of n_max, so a
    # tiny step over a big range can't create an enormous run.
    projected_points = (n_max - n_min) // step + 1
    if projected_points > MAX_DATA_POINTS:
        step = max(step, (n_max - n_min) // MAX_DATA_POINTS)
        warnings.append(
            f"'step' increased to {step} to cap the run at "
            f"~{MAX_DATA_POINTS} data points."
        )

    input_sizes = list(range(n_min, n_max + 1, step))
    if not input_sizes:
        input_sizes = [n_min]

    # --- time the algorithm at each input size ---
    times = []
    for n in input_sizes:
        start = time.perf_counter()
        algorithm(n)
        times.append(time.perf_counter() - start)

    # --- plot & save a snapshot ---
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(input_sizes, times, "o-", color="#2563eb")
    ax.set_xlabel("Input size (n)")
    ax.set_ylabel("Running time (seconds)")
    ax.set_title(f"{algo_name} time complexity — {config['complexity']}")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{algo_name}_{timestamp}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=150)

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=150)
    plt.close(fig)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return jsonify({
        "algo": algo_name,
        "complexity": config["complexity"],
        "n_min": n_min,
        "n_max": n_max,
        "step": step,
        "points": [
            {"n": n, "time_seconds": t} for n, t in zip(input_sizes, times)
        ],
        "image_snapshot_path": filepath,
        "image_base64": image_base64,
        "warnings": warnings,
    })


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Time complexity visualizer. GET /algorithms for the "
                    "supported list, or GET /analyze to run one.",
        "example": "/analyze?algo=linear_search&step=10&n_max=10000",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

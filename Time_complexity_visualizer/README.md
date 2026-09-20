# Time Complexity Visualizer

A small Flask server that runs an algorithm across a range of input
sizes, times each run, and returns both the raw timing data and a
chart (as a base64-encoded PNG) showing running time vs. input size.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The server listens on `http://localhost:8000`.

## Endpoint

### `GET /analyze`

| Query param | Required | Description |
|---|---|---|
| `algo` | yes | Algorithm name, e.g. `linear_search`. See `/algorithms` for the full list. |
| `step` | no (default `1`) | Step size between input sizes. |
| `n_max` | no (default `100`) | Largest input size to test. `n_min` is always `0`. Accepts thousands separators, e.g. `10,000`. |

**Example**

```
http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10000
```

**Response**

```json
{
  "algo": "linear_search",
  "complexity": "O(n)",
  "n_min": 0,
  "n_max": 10000,
  "step": 10,
  "points": [
    {"n": 0, "time_seconds": 0.0000012},
    {"n": 10, "time_seconds": 0.0000021}
  ],
  "image_snapshot_path": "/path/to/snapshots/linear_search_20260101_120000.png",
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "warnings": []
}
```

`image_snapshot_path` points at a PNG saved under `snapshots/` next
to `app.py`; `image_base64` is the same image encoded for direct use
in a browser (`<img src="data:image/png;base64,...">`) or an API
client.

### `GET /algorithms`

Lists every supported algorithm with its Big-O complexity and the
safe maximum `n` the server allows for it (see **Safety limits**
below).

## Supported algorithms

| `algo` value | Complexity |
|---|---|
| `linear_search` | O(n) |
| `binary_search` | O(log n) |
| `bubble_sort` | O(n²) |
| `nested_loops` | O(n²) |
| `merge_sort` | O(n log n) |
| `quick_sort` | O(n log n) average |
| `matrix_multiplication` | O(n³) |
| `fibonacci_recursive` | O(2ⁿ) |

That's the 4 required algorithms (linear search, binary search,
bubble sort, nested loops) plus 4 extra (merge sort, quick sort,
matrix multiplication, naive recursive Fibonacci).

## Safety limits

Some of these algorithms grow fast enough that an unbounded `n_max`
would make a single request take minutes (or longer). To keep the
server responsive:

- Each algorithm has a **max `n`** in `algorithms.py`'s
  `ALGORITHM_CONFIG` (e.g. 150 for matrix multiplication, 32 for
  recursive Fibonacci). A request asking for more is silently
  clamped, and a note is added to the response's `warnings` list.
- The number of `(n, time)` samples in a single request is capped at
  `MAX_DATA_POINTS` (300) in `app.py`. If `step` would produce more
  than that, `step` is increased automatically and a warning is
  returned.

## Fixes from the original prototype

The original script this was built from had a few bugs that would
have prevented it from running at all, and used an interactive,
GUI-based plotting flow that doesn't work in a server process:

- `matplotlib.use('TkAgg')` was called before `matplotlib` itself was
  imported, and needs a display — not available on a server. Swapped
  for the headless `Agg` backend.
- `range(n_min, n_max, + n_step, n_step)` passed 4 arguments to
  `range()`, which only accepts up to 3.
- `line, ax.plot([], [], 'o-')` is a tuple-unpacking bug (missing
  `=`); it would raise `TypeError`.
- `plt.ion()` / `plt.pause()` / `plt.show()` open an interactive
  window and block — replaced with building the figure once,
  saving it to disk, and base64-encoding it for the JSON response.

## Project structure

```
time_complexity_visualizer/
├── app.py            # Flask server, /analyze and /algorithms routes
├── algorithms.py      # algorithm implementations + complexity/limit registry
├── requirements.txt
├── README.md
└── snapshots/          # PNG snapshots saved here on each /analyze call
```

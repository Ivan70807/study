"""
Simple arithmetic HTTP server.

Endpoints:
    GET /add?a=5&b=3
    GET /subtract?a=5&b=3
    GET /multiply?a=5&b=3
    GET /divide?a=5&b=3

Each returns JSON like:
    {"a": 5, "b": 3, "operation": "addition", "result": 8}

Run:
    calculator_server.py

Then open in your browser or curl:
    http://localhost:5000/add?a=5&b=3
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Arithmetic functions

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b


# Maps the URL path to (function, operation name)
OPERATIONS = {
    "/add": (add, "addition"),
    "/subtract": (subtract, "subtraction"),
    "/multiply": (multiply, "multiplication"),
    "/divide": (divide, "division"),
}

# HTTP request handler

class CalculatorHandler(BaseHTTPRequestHandler):

    def _send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path not in OPERATIONS:
            self._send_json(404, {"error": f"Unknown endpoint '{path}'. "
                                            f"Use one of: {list(OPERATIONS.keys())}"})
            return

        func, operation_name = OPERATIONS[path]

        # Validate query params
        if "a" not in query or "b" not in query:
            self._send_json(400, {"error": "Both 'a' and 'b' query parameters are required."})
            return

        try:
            a = float(query["a"][0])
            b = float(query["b"][0])
            # Show as int when the value is a whole number, e.g. 5 instead of 5.0
            a_clean = int(a) if a.is_integer() else a
            b_clean = int(b) if b.is_integer() else b
        except ValueError:
            self._send_json(400, {"error": "'a' and 'b' must be numbers."})
            return

        try:
            result = func(a_clean, b_clean)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
        except ZeroDivisionError as e:
            self._send_json(400, {"error": str(e)})
            return

        self._send_json(200, {
            "a": a_clean,
            "b": b_clean,
            "operation": operation_name,
            "result": result,
        })

    def log_message(self, format, *args):
        # Slightly cleaner console logging
        print(f"{self.address_string()} - {format % args}")

# Entry point

def main():
    host = "localhost"
    port = 5000
    server = HTTPServer((host, port), CalculatorHandler)
    print(f"Calculator server running at http://{host}:{port}")
    print("Try, for example:")
    print(f"  http://{host}:{port}/add?a=5&b=3")
    print(f"  http://{host}:{port}/subtract?a=5&b=3")
    print(f"  http://{host}:{port}/multiply?a=5&b=3")
    print(f"  http://{host}:{port}/divide?a=5&b=3")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()


if __name__ == "__main__":
    main()

import random
import sys

from stack import Stack, StackEmptyError
from queue_ds import Queue


sys.setrecursionlimit(10_000)


def linear_search(n):
    """O(n) — scan a list of size n for a value that isn't in it
    (worst case: the loop never breaks early)."""
    arr = list(range(n))
    target = -1
    for value in arr:
        if value == target:
            return True
    return False


def binary_search(n):
    """O(log n) — binary search a sorted list of size n for a value
    that isn't in it (worst case)."""
    arr = list(range(n))
    target = -1
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return True
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False


def bubble_sort(n):
    """O(n^2) — bubble sort a reverse-sorted list of size n
    (worst case)."""
    arr = list(range(n, 0, -1))
    for i in range(len(arr)):
        swapped = False
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def nested_loops(n):
    """O(n^2) — a bare double loop with no sorting/searching
    overhead, useful as a 'pure' quadratic baseline."""
    total = 0
    for i in range(n):
        for j in range(n):
            total += 1
    return total


def merge_sort(n):
    """O(n log n) — merge sort a randomly shuffled list of size n."""
    arr = list(range(n))
    random.shuffle(arr)
    return _merge_sort(arr)


def _merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = _merge_sort(arr[:mid])
    right = _merge_sort(arr[mid:])
    return _merge(left, right, arr)


def _merge(left, right, out):
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out[k] = left[i]
            i += 1
        else:
            out[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        out[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        out[k] = right[j]
        j += 1
        k += 1
    return out


def quick_sort(n):
    """O(n log n) average — quicksort a randomly shuffled list of
    size n (last-element pivot)."""
    arr = list(range(n))
    random.shuffle(arr)
    _quick_sort(arr, 0, len(arr) - 1)
    return arr


def _quick_sort(arr, low, high):
    if low < high:
        p = _partition(arr, low, high)
        _quick_sort(arr, low, p - 1)
        _quick_sort(arr, p + 1, high)


def _partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def matrix_multiplication(n):
    """O(n^3) — multiply two n x n matrices of random ints using
    plain triple-nested loops. n is capped low (see ALGORITHM_CONFIG)
    since cubic growth gets expensive fast."""
    a = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
    b = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s += a[i][k] * b[k][j]
            result[i][j] = s
    return result


def fibonacci_recursive(n):
    """O(2^n) — naive recursive Fibonacci. n is capped very low (see
    ALGORITHM_CONFIG) because this blows up almost immediately."""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def stack_push_pop(n):
    """O(n) — push n items onto a Stack, then pop them all back off."""
    s = Stack()
    for i in range(n):
        s.push(i)
    while not s.is_empty():
        s.pop()


def stack_balanced_parentheses(n):
    """O(n) — build a balanced string of 2n parentheses, e.g.
    "(((...)))", and validate it using a Stack. Classic textbook use
    of a stack: push on '(', pop on ')', valid iff the stack empties
    out exactly at the end."""
    text = "(" * n + ")" * n
    s = Stack()
    for ch in text:
        if ch == "(":
            s.push(ch)
        else:
            try:
                s.pop()
            except StackEmptyError:
                return False
    return s.is_empty()


def queue_enqueue_dequeue(n):
    """O(n) — enqueue n items onto a Queue, then dequeue them all."""
    q = Queue()
    for i in range(n):
        q.enqueue(i)
    while not q.is_empty():
        q.dequeue()


def queue_bfs_traversal(n):
    """O(n) — breadth-first traversal of a simple n-node chain graph
    (0 -> 1 -> 2 -> ... -> n-1), using a Queue to hold the frontier.
    A straight chain keeps this O(n) rather than O(n + edges)."""
    if n <= 0:
        return set()
    graph = {i: [i + 1] for i in range(n - 1)}
    graph[n - 1] = []

    visited = {0}
    q = Queue()
    q.enqueue(0)
    while not q.is_empty():
        node = q.dequeue()
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                q.enqueue(neighbor)
    return visited


# Registry: maps the `algo` query-param value to its runner function,
# a human-readable Big-O label, and a safe maximum n so the server
# never gets stuck running something outrageous (e.g. fibonacci of
# 10,000, or an O(n^3) matrix multiply at n=10,000).
ALGORITHM_CONFIG = {
    "linear_search": {
        "func": linear_search,
        "complexity": "O(n)",
        "max_n": 200_000,
    },
    "binary_search": {
        "func": binary_search,
        "complexity": "O(log n)",
        "max_n": 1_000_000,
    },
    "bubble_sort": {
        "func": bubble_sort,
        "complexity": "O(n^2)",
        "max_n": 3_000,
    },
    "nested_loops": {
        "func": nested_loops,
        "complexity": "O(n^2)",
        "max_n": 3_000,
    },
    "merge_sort": {
        "func": merge_sort,
        "complexity": "O(n log n)",
        "max_n": 200_000,
    },
    "quick_sort": {
        "func": quick_sort,
        "complexity": "O(n log n) avg",
        "max_n": 5_000,
    },
    "matrix_multiplication": {
        "func": matrix_multiplication,
        "complexity": "O(n^3)",
        "max_n": 150,
    },
    "fibonacci_recursive": {
        "func": fibonacci_recursive,
        "complexity": "O(2^n)",
        "max_n": 32,
    },
    "stack_push_pop": {
        "func": stack_push_pop,
        "complexity": "O(n)",
        "max_n": 100_000,
    },
    "stack_balanced_parentheses": {
        "func": stack_balanced_parentheses,
        "complexity": "O(n)",
        "max_n": 100_000,
    },
    "queue_enqueue_dequeue": {
        "func": queue_enqueue_dequeue,
        "complexity": "O(n)",
        "max_n": 100_000,
    },
    "queue_bfs_traversal": {
        "func": queue_bfs_traversal,
        "complexity": "O(n)",
        "max_n": 100_000,
    },
}

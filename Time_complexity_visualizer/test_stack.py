

import unittest

from stack import Stack, StackEmptyError


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    # --- basic state ---

    def test_new_stack_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(len(self.stack), 0)

    def test_push_increases_size(self):
        self.stack.push(1)
        self.assertEqual(self.stack.size(), 1)
        self.assertFalse(self.stack.is_empty())

        self.stack.push(2)
        self.assertEqual(self.stack.size(), 2)

    # --- LIFO ordering ---

    def test_pop_returns_last_pushed_item_lifo(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)

    def test_pop_decreases_size(self):
        self.stack.push("a")
        self.stack.push("b")
        self.stack.pop()
        self.assertEqual(self.stack.size(), 1)

    def test_interleaved_push_and_pop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.stack.push(3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 1)
        self.assertTrue(self.stack.is_empty())

    # --- peek ---

    def test_peek_returns_top_without_removing(self):
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.peek(), 20)
        self.assertEqual(self.stack.size(), 2)  # unchanged by peek

    def test_peek_empty_raises(self):
        with self.assertRaises(StackEmptyError):
            self.stack.peek()

    # --- error handling ---

    def test_pop_empty_raises(self):
        with self.assertRaises(StackEmptyError):
            self.stack.pop()

    def test_pop_until_empty_then_raises(self):
        self.stack.push(1)
        self.stack.pop()
        with self.assertRaises(StackEmptyError):
            self.stack.pop()

    # --- data flexibility ---

    def test_push_pop_mixed_types(self):
        self.stack.push(1)
        self.stack.push("two")
        self.stack.push([3])
        self.stack.push(None)
        self.assertIsNone(self.stack.pop())
        self.assertEqual(self.stack.pop(), [3])
        self.assertEqual(self.stack.pop(), "two")
        self.assertEqual(self.stack.pop(), 1)

    # --- scale ---

    def test_large_number_of_operations(self):
        n = 10_000
        for i in range(n):
            self.stack.push(i)
        self.assertEqual(self.stack.size(), n)
        for expected in reversed(range(n)):
            self.assertEqual(self.stack.pop(), expected)
        self.assertTrue(self.stack.is_empty())

    # --- dunder / repr ---

    def test_len_matches_size(self):
        for i in range(5):
            self.stack.push(i)
        self.assertEqual(len(self.stack), self.stack.size())

    def test_repr_does_not_crash_and_is_informative(self):
        self.stack.push(1)
        self.stack.push(2)
        text = repr(self.stack)
        self.assertIn("Stack", text)


if __name__ == "__main__":
    unittest.main()



import unittest

from queue_ds import Queue, QueueEmptyError


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    # --- basic state ---

    def test_new_queue_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)
        self.assertEqual(len(self.queue), 0)

    def test_enqueue_increases_size(self):
        self.queue.enqueue(1)
        self.assertEqual(self.queue.size(), 1)
        self.assertFalse(self.queue.is_empty())

        self.queue.enqueue(2)
        self.assertEqual(self.queue.size(), 2)

    # --- FIFO ordering ---

    def test_dequeue_returns_first_enqueued_item_fifo(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 3)

    def test_dequeue_decreases_size(self):
        self.queue.enqueue("a")
        self.queue.enqueue("b")
        self.queue.dequeue()
        self.assertEqual(self.queue.size(), 1)

    def test_interleaved_enqueue_and_dequeue(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.dequeue(), 1)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 3)
        self.assertTrue(self.queue.is_empty())

    # --- peek ---

    def test_peek_returns_front_without_removing(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.peek(), 10)
        self.assertEqual(self.queue.size(), 2)  # unchanged by peek

    def test_peek_empty_raises(self):
        with self.assertRaises(QueueEmptyError):
            self.queue.peek()

    # --- error handling ---

    def test_dequeue_empty_raises(self):
        with self.assertRaises(QueueEmptyError):
            self.queue.dequeue()

    def test_dequeue_until_empty_then_raises(self):
        self.queue.enqueue(1)
        self.queue.dequeue()
        with self.assertRaises(QueueEmptyError):
            self.queue.dequeue()

    # --- data flexibility ---

    def test_enqueue_dequeue_mixed_types(self):
        self.queue.enqueue(1)
        self.queue.enqueue("two")
        self.queue.enqueue([3])
        self.queue.enqueue(None)
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.dequeue(), "two")
        self.assertEqual(self.queue.dequeue(), [3])
        self.assertIsNone(self.queue.dequeue())

    # --- scale ---

    def test_large_number_of_operations(self):
        n = 10_000
        for i in range(n):
            self.queue.enqueue(i)
        self.assertEqual(self.queue.size(), n)
        for expected in range(n):
            self.assertEqual(self.queue.dequeue(), expected)
        self.assertTrue(self.queue.is_empty())

    # --- dunder / repr ---

    def test_len_matches_size(self):
        for i in range(5):
            self.queue.enqueue(i)
        self.assertEqual(len(self.queue), self.queue.size())

    def test_repr_does_not_crash_and_is_informative(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        text = repr(self.queue)
        self.assertIn("Queue", text)


if __name__ == "__main__":
    unittest.main()

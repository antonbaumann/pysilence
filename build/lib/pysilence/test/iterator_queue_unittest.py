import random
import unittest

from silence_detection import window


class TestRingQueue(unittest.TestCase):
    def test_add(self):
        test_lst = [random.randint(-300, 300) for _ in range(200)]
        cache = window.RingQueue(3)

        # init queue
        for i in range(cache.size - 1):
            cache.add(test_lst[i])

        for i in range(cache.size - 1, len(test_lst)):
            cache.add(test_lst[i])
            self.assertEqual(set(cache.data), set(test_lst[i - cache.size + 1:i+1]))

    def test_get_energy(self):
        test_lst = [3, 6, 7, 2, 4, 9, 0]
        expected = [
            sum([3, 6, 7]) / 3,
            sum([6, 7, 2]) / 3,
            sum([7, 2, 4]) / 3,
            sum([2, 4, 9]) / 3,
            sum([4, 9, 0]) / 3,
        ]
        cache = window.RingQueue(3)

        # init queue
        for i in range(cache.size - 1):
            cache.add(test_lst[i])

        self.assertListEqual(cache.data.tolist(), [3., 6., 0.])

        for i in range(cache.size - 1, len(test_lst)):
            cache.add(test_lst[i])
            self.assertEqual(cache.get_energy(), expected[i-(cache.size-1)])


if __name__ == '__main__':
    unittest.main()

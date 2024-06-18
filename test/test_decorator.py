    # tests/test_decorator.py

import unittest
from pysniffer import benchmark

class TestBenchmarkDecorator(unittest.TestCase):
    def test_benchmark(self):
        @benchmark()
        def sample_function():
            return "Hello, World!"

        result = sample_function()
        self.assertEqual(result, "Hello, World!")

if __name__ == '__main__':
    unittest.main()

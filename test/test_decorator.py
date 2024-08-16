import pytest
import asyncio
from src.pysniffer import benchmark

def test_benchmark():
    @benchmark()
    def sample_function():
        return "Hello, World!"

    result = sample_function()
    assert result == "Hello, World!"

    @benchmark()
    def test_funtion():
        for _ in range(10000):
            pass
        return "Hello, World!"

    result = test_funtion()
    assert result == "Hello, World!"

    @benchmark()
    def example_funtion():
        for _ in range(10000):
            pass
        return "Hello, World!"

    result = example_funtion()
    assert result == "Hello, World!"

    @benchmark()
    def time_test():
        import time
        time.sleep(3)
        return "_"

    result = time_test()
    assert result == "_"

def test_async_profiling():
    """Testing async benchmarking features"""

    @benchmark(lines_to_print=100)
    async def some_async_function():
        await asyncio.sleep(2)
        return "_"

    result = asyncio.run(some_async_function())
    assert result == "_"

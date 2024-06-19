import pytest
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
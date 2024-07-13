# PySniffer

[![pypi](https://img.shields.io/pypi/v/pysniffer.svg)](https://pypi.org/project/pysniffer/)
[![Release](https://img.shields.io/github/release/dhananjayanonline/pysniffer.svg)](https://github.com/dhananjayaonline/pysniffer/releases/latest)
[![Release](https://github.com/dhananjayanonline/pysniffer/actions/workflows/releasebuild.yml/badge.svg)](https://github.com/dhananjayanonline/pysniffer/actions/workflows/releasebuild.yml)

## Overview
PySniffer is a powerful and easy-to-use Python package designed to profile and measure the performance of functions. This tool is invaluable for developers who need to optimize their code by gaining insights into execution time, CPU time, and peak memory usage. The decorator automatically logs detailed profiling data, allowing for easy analysis and debugging.

## Features
- **Execution Time Measurement**: Captures the total wall-clock time taken for the function to execute.
- **CPU Time Measurement**: Records the CPU time consumed during the function execution, identifying CPU-bound operations.
- **Memory Usage Profiling**: Tracks and logs the peak memory usage, providing insights into the memory efficiency of the function.
- **Profiling Statistics**: Utilizes the `cProfile` module to gather detailed statistics on function calls, sorted by various criteria such as cumulative time.
- **Customizable Logging**:
  - **Log Level**: Set the verbosity of the logs with different logging levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
  - **Log File**: Specify the log file path to store the profiling data.
  - **Append or Overwrite**: Choose whether to append to the existing log file or overwrite it with new data.
- **Flexible Output**: Logs can be directed to both the console and a log file, providing flexibility in how the profiling information is consumed and stored.

## Installation
You can install PySniffer from PyPI using pip:

```bash
pip install pysniffer
```

## Usage
To use the benchmarking decorator, simply apply it to any function you want to profile. Customize the behavior using the decorator's parameters to suit your specific needs.

## Quick Usage
```python
from pysniffer import benchmark

@benchmark
def example_function():
    # Function implementation
    pass

example_function()
```

### Full Usage Example
For more customization, you can specify parameters as follows:
```python
import logging
from pysniffer import benchmark

@benchmark(sort_by=pstats.SortKey.TIME, lines_to_print=20, log_level=logging.DEBUG, log_file="detailed_profile.log", append_log=False)
def example_function():
    # Function implementation
    pass

example_function()
```

### Parameters
- **sort_by (pstats.SortKey)**: Sorting key for profiling statistics. Default is `pstats.SortKey.CUMULATIVE`.
- **lines_to_print (int)**: Number of lines of profiling statistics to print. Default is 10.
- **log_level (logging.LEVEL)**: Logging level for profiling data. Default is `logging.INFO`.
- **log_file (str)**: Path to the log file for profiling data. Default is `"profile.log"`.
- **append_log (bool)**: Whether to append profiling data to the log file or overwrite it. Default is `True`.

### Benefits
- **Performance Optimization**: Identify bottlenecks and optimize the performance of your functions.
- **Resource Management**: Monitor and manage memory usage effectively.
- **Detailed Insights**: Gain in-depth understanding of function behavior through detailed profiling statistics.
- **Ease of Use**: Simple integration into existing code with customizable parameters for tailored profiling.

## License
PySniffer is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Acknowledgements
This project leverages Python's `cProfile`, `pstats`, and `tracemalloc` modules for profiling and memory tracking.

## Contact
For any questions or suggestions, please feel free to open an issue on the GitHub repository or contact the project maintainers.

---

import time
import tracemalloc
import cProfile
import pstats
import io
import logging
from typing import Callable
from functools import wraps

for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)

logging.getLogger().addHandler(logging.StreamHandler())


def benchmark(
    sort_by: str=pstats.SortKey.CUMULATIVE,
    lines_to_print: int=10,
    log_level: int=logging.INFO,
    log_file: str="profile.log",
    append_log: bool=True,
) -> Callable:
    """
    Decorator that measures and profiles the execution time, CPU time,
    and peak memory usage of a function. Writes profiling data to a log file
    or the console depending on the log_level.

    Args:
        sort_by (pstats.SortKey, optional): Sorting key for profiling statistics.
            Defaults to pstats.SortKey.CUMULATIVE.
        lines_to_print (int, optional): Number of profiling statistics lines to print.
            Defaults to 10.
        log_level (logging.LEVEL, optional): The logging level for profiling data.
            Defaults to logging.INFO.
        log_file (str, optional): Path to the log file for profiling data.
            Defaults to "profile.log".
        append_log (bool, optional): Whether to append profiling data to the log
            file or overwrite it. Defaults to True.

    Returns:
        callable: The decorated function with profiling capabilities.
    """

    def decorator(func):
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Start memory and CPU profiling
            tracemalloc.start()
            pr = cProfile.Profile()
            pr.enable()

            start_time = time.time()
            cpu_start_time = time.process_time()

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Function '{func.__name__}' raised an exception: {e}")
                raise
            finally:
                # Stop profiling
                cpu_end_time = time.process_time()
                end_time = time.time()
                pr.disable()
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                # Capture profiling stats
                s = io.StringIO()
                ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
                ps.print_stats(lines_to_print)

                # Calculate elapsed times and memory usage
                elapsed_time = end_time - start_time
                elapsed_cpu_time = cpu_end_time - cpu_start_time
                memory_usage = peak / 1024

                # Create the log message
                message = (
                    f"🌟 === Function '{func.__name__}' Execution Summary ===\n"
                    f"  - ⏱ Elapsed Time: {elapsed_time:.4f} seconds\n"
                    f"  - ⚙️ CPU Time: {elapsed_cpu_time:.4f} seconds\n"
                    f"  - 📈 Peak Memory Usage: {memory_usage:.2f} KB\n\n"
                    f"💡 === Function Output ===\n"
                    f"{s.getvalue()}"
                )


                logger.log(log_level, message)

                with open(log_file, "a" if append_log else "w") as f:
                    f.write("\n" * 2)
                    f.write(message)
                    f.write("-" * 80 + "\n")

            return result

        return wrapper

    return decorator

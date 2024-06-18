import time
import tracemalloc
import cProfile
import pstats
import io
import logging
from functools import wraps

for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)

logging.getLogger().addHandler(logging.StreamHandler())



def benchmark(sort_by=pstats.SortKey.CUMULATIVE, lines_to_print=10, log_level=logging.INFO, log_file="profile.log", append_log=True):
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
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            logger = logging.getLogger(__name__)
            logger.setLevel(log_level)

            tracemalloc.start()
            pr = cProfile.Profile()
            pr.enable()

            start_time = time.time()
            cpu_start_time = time.process_time()

            result = func(*args, **kwargs)

            cpu_end_time = time.process_time()
            end_time = time.time()

            pr.disable()
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
            ps.print_stats(lines_to_print)


            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            elapsed_time = end_time - start_time
            elapsed_cpu_time = cpu_end_time - cpu_start_time
            memory_usage = peak / 1024  

            message = f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds and CPU time taken is {elapsed_cpu_time:.4f} seconds\n"
            message += f"Peak memory usage was {memory_usage:.2f} KB\n"
            message += s.getvalue()

            logger.log(log_level, message)

            with open(log_file, "a" if append_log else "w") as f:
                f.write("\n \n")
                f.write(message)
                f.write("----------------------------------------------------------\n")

            return result
        return wrapper
    return decorator
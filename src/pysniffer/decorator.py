import time
import tracemalloc
import cProfile
import pstats
import io
import logging
from inspect import iscoroutinefunction
from typing import Callable
from functools import wraps
from .interfaces import TraceObject, AnalysisResult

def __make_trace(start_trace:bool=False) -> TraceObject:
    # Start memory and CPU profiling
    tracemalloc.start()
    pr = cProfile.Profile()

    start_time = time.time()
    cpu_start_time = time.process_time()
    if start_trace:
        pr.enable()
    return {
        "pr": pr, "cpu_start_time": cpu_start_time, "start_time": start_time
    }

def __analyse_trace(traces:TraceObject, sort_by:str, lines_to_print:int, stop_trace:bool=False) -> AnalysisResult:
    # Stop profiling
    if stop_trace:
        traces["pr"].disable()
    cpu_end_time = time.process_time()
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Capture profiling stats
    s = io.StringIO()
    ps = pstats.Stats(traces['pr'], stream=s).sort_stats(sort_by)
    ps.print_stats(lines_to_print)

    # Calculate elapsed times and memory usage
    elapsed_time = end_time - traces["start_time"]
    elapsed_cpu_time = cpu_end_time - traces['cpu_start_time']
    memory_usage = peak / 1024

    return {
        "elapsed_time": elapsed_time, "elapsed_cpu_time": elapsed_cpu_time,
        "memory_usage": memory_usage, "process_trace": s,
    }

def __dump_analysis_report(
    function_name:str,
    analysis: AnalysisResult,
    logger:logging.Logger,
    log_level: int=logging.INFO,
    log_file: str="profile.log",
    append_log: bool=True
):
    message = (
        f"🌟 === Function '{function_name}' Execution Summary ===\n"
        f"  - ⏱ Elapsed Time: {analysis['elapsed_time']:.4f} seconds\n"
        f"  - ⚙️ CPU Time: {analysis['elapsed_cpu_time']:.4f} seconds\n"
        f"  - 📈 Peak Memory Usage: {analysis['memory_usage']:.2f} KB\n\n"
        f"💡 === Function Output ===\n"
        f"{analysis['process_trace'].getvalue()}"
    )

    logger.log(log_level, message)

    with open(log_file, "a" if append_log else "w") as f:
        f.write("\n" * 2)
        f.write(message)
        f.write("-" * 80 + "\n")


def benchmark(
    sort_by: str=pstats.SortKey.CUMULATIVE,
    lines_to_print: int=10,
    log_level: int=logging.INFO,
    log_file: str="profile.log",
    append_log: bool=True,
    stop_other_loggers: bool=False
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
        stop_other_loggers (bool, optional): Whether to disable all other loggers binded
            to python logger. Defaults to False.

    Returns:
        callable: The decorated function with profiling capabilities.
    """

    if stop_other_loggers:
        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)
        logging.getLogger().addHandler(logging.StreamHandler())

    def decorator(func):
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        wrapper_fun = None

        if iscoroutinefunction(func):
            # handlig async function call
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                trace = __make_trace()
                trace['pr'].enable()
                try:
                    result = await func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Function '{func.__name__}' raised an exception: {e}")
                    raise e
                finally:
                    trace['pr'].disable()
                    analysis = __analyse_trace(trace, sort_by=sort_by, lines_to_print=lines_to_print)
                    __dump_analysis_report(func.__name__, analysis, logger, log_level, log_file, append_log)
                return result

            wrapper_fun = async_wrapper

        else:
            # synchronous wrapper
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                trace = __make_trace()
                trace['pr'].enable()
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Function '{func.__name__}' raised an exception: {e}")
                    raise e
                finally:
                    trace['pr'].disable()
                    analysis = __analyse_trace(trace, sort_by=sort_by, lines_to_print=lines_to_print)
                    __dump_analysis_report(func.__name__, analysis, logger, log_level, log_file, append_log)
                return result

            wrapper_fun = sync_wrapper

        return wrapper_fun

    return decorator

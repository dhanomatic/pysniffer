import io
import cProfile
from typing import TypedDict

class TraceObject(TypedDict):
    pr: cProfile.Profile
    start_time: float
    cpu_start_time: float

class AnalysisResult(TypedDict):
    elapsed_time: float
    elapsed_cpu_time: float
    memory_usage: float
    process_trace: io.StringIO

import pandas as pd
import pytest
from agentic_data_storyteller.agents.profiler_agent import DataProfilerAgent

def test_profiler_basic_stats():
    df = pd.DataFrame({
        "revenue": [100.0, 200.0, 300.0, 1000.0],
        "category": ["A", "B", "A", "B"],
        "date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"]
    })
    profiler = DataProfilerAgent()
    profile = profiler.profile(df)

    assert profile.row_count == 4
    assert profile.column_count == 3
    assert "revenue" in profile.numeric_columns
    assert "category" in profile.categorical_columns
    assert "revenue" in profile.columns
    assert profile.columns["revenue"].stats["mean"] == 400.0

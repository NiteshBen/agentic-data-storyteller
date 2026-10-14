import pandas as pd
import pytest
from agentic_data_storyteller.agents.profiler_agent import DataProfilerAgent
from agentic_data_storyteller.agents.insight_agent import InsightDiscoveryAgent

def test_insight_driver_discovery():
    df = pd.DataFrame({
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        "cat": ["Alpha"] * 8 + ["Beta"] * 2
    })
    profiler = DataProfilerAgent()
    profile = profiler.profile(df)
    
    agent = InsightDiscoveryAgent()
    report = agent.discover(df, profile)

    assert len(report.key_drivers) >= 1
    assert report.key_drivers[0]["feature_a"] in ["x", "y"]
    assert report.key_drivers[0]["correlation"] >= 0.99
    assert len(report.insights) >= 1

import os
import pandas as pd
import pytest
from agentic_data_storyteller.agents.profiler_agent import DataProfilerAgent
from agentic_data_storyteller.agents.insight_agent import InsightDiscoveryAgent
from agentic_data_storyteller.agents.visualizer_agent import DataVisualizerAgent

def test_visualizer_generates_html(tmp_path):
    df = pd.DataFrame({
        "sales": [100, 200, 150, 300],
        "category": ["Tech", "Home", "Tech", "Office"]
    })
    profiler = DataProfilerAgent()
    profile = profiler.profile(df)
    
    agent = InsightDiscoveryAgent()
    report = agent.discover(df, profile)

    vis = DataVisualizerAgent()
    out_html = str(tmp_path / "dashboard.html")
    vis.generate_dashboard(df, profile, report, out_html)

    assert os.path.exists(out_html)
    with open(out_html, "r", encoding="utf-8") as f:
        html = f.read()
    assert "Executive Data Storyboard" in html
    assert "Category Distribution" in html

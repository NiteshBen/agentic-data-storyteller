import os
import pandas as pd
from agentic_data_storyteller.orchestrator import StorytellerOrchestrator

def test_full_pipeline_run(tmp_path):
    df = pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"],
        "category": ["A", "B", "A", "C", "A"],
        "revenue": [120.0, 340.0, 110.0, 500.0, 230.0],
        "profit": [40.0, 120.0, 35.0, 210.0, 90.0]
    })
    
    out_dir = str(tmp_path / "artifacts")
    orchestrator = StorytellerOrchestrator(output_dir=out_dir)
    result = orchestrator.run_pipeline(df)

    assert os.path.exists(result.html_dashboard_path)
    assert os.path.exists(result.infographic_svg_path)
    assert os.path.exists(os.path.join(out_dir, "EXECUTIVE_STORY.md"))
    assert os.path.exists(os.path.join(out_dir, "LINKEDIN_POST.md"))
    assert "Agentic Data Storyteller" in result.linkedin_post

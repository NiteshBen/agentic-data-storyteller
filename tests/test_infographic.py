import os
from agentic_data_storyteller.utils.infographic_generator import InfographicGenerator

def test_infographic_generates_svg(tmp_path):
    svg_path = str(tmp_path / "card.svg")
    kpis = [
        {"label": "Revenue", "value": "$1.2M", "sub": "Gross"},
        {"label": "Orders", "value": "15,420", "sub": "Total Count"}
    ]
    takeaways = [
        "Electronics leads all category performance by 42%.",
        "Direct search delivers the highest margin conversion."
    ]

    out = InfographicGenerator.generate_svg(
        title="Test Storyboard",
        subtitle="Sample Executive Summary Subtitle",
        kpis=kpis,
        takeaways=takeaways,
        output_path=svg_path
    )

    assert os.path.exists(svg_path)
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "<svg" in content
    assert "Test Storyboard" in content
    assert "Electronics leads all category performance" in content

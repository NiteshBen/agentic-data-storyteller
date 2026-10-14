import os
import pandas as pd
from typing import Dict, Any, Optional
from .agents.profiler_agent import DataProfilerAgent
from .agents.insight_agent import InsightDiscoveryAgent
from .agents.visualizer_agent import DataVisualizerAgent
from .agents.storyteller_agent import StorytellerAgent
from .utils.infographic_generator import InfographicGenerator
from .models.schema import StoryOutput

class StorytellerOrchestrator:
    """
    Coordinates the collaborative multi-agent data storytelling pipeline.
    """

    def __init__(self, output_dir: str = "artifacts"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.profiler = DataProfilerAgent()
        self.insight_engine = InsightDiscoveryAgent()
        self.visualizer = DataVisualizerAgent()
        self.storyteller = StorytellerAgent()

    def run_pipeline(self, csv_or_df: Any, repo_url: str = "https://github.com/NiteshBen/agentic-data-storyteller") -> StoryOutput:
        # 1. Ingest Data
        if isinstance(csv_or_df, str):
            df = pd.read_csv(csv_or_df)
        elif isinstance(csv_or_df, pd.DataFrame):
            df = csv_or_df
        else:
            raise ValueError("Input must be a CSV file path or pandas DataFrame")

        # 2. Agent 1: Statistical Profiling
        profile = self.profiler.profile(df)

        # 3. Agent 2: Insight & Driver Discovery
        insights = self.insight_engine.discover(df, profile)

        # 4. Agent 3: Visual Dashboard Generation
        dashboard_path = os.path.join(self.output_dir, "executive_dashboard.html")
        self.visualizer.generate_dashboard(df, profile, insights, dashboard_path)

        # 5. Agent 4 & Utility: Vector Infographic Generation
        infographic_path = os.path.join(self.output_dir, "executive_infographic.svg")
        
        # Build KPI badges
        kpis = [
            {"label": "Records Scanned", "value": f"{profile.row_count:,}", "sub": "Total Data Points"},
            {"label": "Dimensions", "value": str(profile.column_count), "sub": "Features Analyzed"},
            {"label": "Key Drivers", "value": str(len(insights.key_drivers)), "sub": "Stat Correlations"},
            {"label": "Core Insights", "value": str(len(insights.insights)), "sub": "Strategic Signals"}
        ]
        
        takeaways = [item.title for item in insights.insights[:3]]
        if not takeaways:
            takeaways = ["Data profile completed with high statistical fidelity."]

        InfographicGenerator.generate_svg(
            title="Executive Data Storyboard",
            subtitle=insights.summary[:95] + "..." if len(insights.summary) > 95 else insights.summary,
            kpis=kpis,
            takeaways=takeaways,
            output_path=infographic_path
        )

        # 6. Agent 4: Storytelling & Social Formulation
        story_output = self.storyteller.generate_stories(
            profile=profile,
            insights=insights,
            dashboard_path=dashboard_path,
            infographic_path=infographic_path,
            repo_url=repo_url
        )

        # Write output files
        story_md_path = os.path.join(self.output_dir, "EXECUTIVE_STORY.md")
        with open(story_md_path, "w", encoding="utf-8") as f:
            f.write(story_output.executive_story_markdown)

        linkedin_md_path = os.path.join(self.output_dir, "LINKEDIN_POST.md")
        with open(linkedin_md_path, "w", encoding="utf-8") as f:
            f.write(story_output.linkedin_post)

        return story_output

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
from ..models.schema import DatasetProfile, InsightReport

class DataVisualizerAgent:
    """
    Autonomous agent responsible for creating interactive visualizations
    and assembling an executive HTML dashboard.
    """

    def __init__(self, name: str = "DataVisualizerAgent"):
        self.name = name

    def generate_dashboard(
        self,
        df: pd.DataFrame,
        profile: DatasetProfile,
        insights: InsightReport,
        output_html_path: str
    ) -> str:
        chart_divs: List[str] = []

        # 1. Categorical Breakdown Chart
        if profile.categorical_columns:
            cat_col = profile.categorical_columns[0]
            val_counts = df[cat_col].value_counts().head(8).reset_index()
            val_counts.columns = [cat_col, "Count"]
            
            fig_cat = px.bar(
                val_counts,
                x=cat_col,
                y="Count",
                title=f"Category Distribution: {cat_col}",
                template="plotly_dark",
                color="Count",
                color_continuous_scale="Viridis"
            )
            fig_cat.update_layout(
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                margin=dict(l=40, r=40, t=50, b=40)
            )
            chart_divs.append(fig_cat.to_html(full_html=False, include_plotlyjs="cdn"))

        # 2. Correlation Heatmap
        if len(profile.numeric_columns) >= 2:
            num_sub = profile.numeric_columns[:8]
            corr_matrix = df[num_sub].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=".2f",
                aspect="auto",
                title="Multivariate Correlation Matrix",
                template="plotly_dark",
                color_continuous_scale="RdBu_r"
            )
            fig_corr.update_layout(
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                margin=dict(l=40, r=40, t=50, b=40)
            )
            chart_divs.append(fig_corr.to_html(full_html=False, include_plotlyjs=False))

        # 3. Numeric Distribution / Box Plots
        if profile.numeric_columns:
            top_num = profile.numeric_columns[0]
            fig_dist = px.histogram(
                df,
                x=top_num,
                marginal="box",
                title=f"Distribution Profile: {top_num}",
                template="plotly_dark",
                color_discrete_sequence=["#38BDF8"]
            )
            fig_dist.update_layout(
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                margin=dict(l=40, r=40, t=50, b=40)
            )
            chart_divs.append(fig_dist.to_html(full_html=False, include_plotlyjs=False))

        # 4. Temporal Trends (if date column exists)
        if profile.datetime_columns and profile.numeric_columns:
            dt_col = profile.datetime_columns[0]
            num_col = profile.numeric_columns[0]
            try:
                temp_df = df.copy()
                temp_df["_dt"] = pd.to_datetime(temp_df[dt_col], errors="coerce")
                trend_df = temp_df.dropna(subset=["_dt"]).groupby(temp_df["_dt"].dt.to_period("W"))[num_col].mean().reset_index()
                trend_df["_dt"] = trend_df["_dt"].astype(str)
                
                fig_trend = px.line(
                    trend_df,
                    x="_dt",
                    y=num_col,
                    title=f"Weekly Average Trajectory: {num_col}",
                    template="plotly_dark",
                    markers=True
                )
                fig_trend.update_traces(line_color="#10B981")
                fig_trend.update_layout(
                    paper_bgcolor="#111827",
                    plot_bgcolor="#111827",
                    margin=dict(l=40, r=40, t=50, b=40)
                )
                chart_divs.append(fig_trend.to_html(full_html=False, include_plotlyjs=False))
            except Exception:
                pass

        # Build full HTML document
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic Data Storyteller | Executive Dashboard</title>
    <style>
        :root {{
            --bg-color: #0b0f19;
            --card-bg: #111827;
            --border-color: #1f2937;
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent-cyan: #38bdf8;
            --accent-green: #10b981;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            margin: 0;
            padding: 24px;
        }}
        .header {{
            max-width: 1200px;
            margin: 0 auto 24px auto;
            padding: 24px;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }}
        .badge {{
            display: inline-block;
            background-color: rgba(56, 189, 248, 0.15);
            color: var(--accent-cyan);
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}
        h1 {{
            margin: 0 0 8px 0;
            font-size: 28px;
            font-weight: 800;
        }}
        p.subtitle {{
            margin: 0;
            color: var(--text-secondary);
            font-size: 15px;
        }}
        .kpi-row {{
            max-width: 1200px;
            margin: 0 auto 24px auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
        }}
        .kpi-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 20px;
        }}
        .kpi-label {{
            font-size: 12px;
            color: var(--text-secondary);
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        .kpi-value {{
            font-size: 26px;
            font-weight: 800;
            color: var(--accent-cyan);
        }}
        .charts-grid {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
            gap: 20px;
        }}
        .chart-box {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 12px;
            overflow: hidden;
        }}
        .footer {{
            max-width: 1200px;
            margin: 40px auto 0 auto;
            text-align: center;
            font-size: 13px;
            color: var(--text-secondary);
        }}
    </style>
</head>
<body>
    <div class="header">
        <span class="badge">Autonomous Multi-Agent Intelligence</span>
        <h1>Executive Data Storyboard</h1>
        <p class="subtitle">{insights.summary}</p>
    </div>

    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">Total Observations</div>
            <div class="kpi-value">{profile.row_count:,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Features Profiled</div>
            <div class="kpi-value">{profile.column_count}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Key Drivers Detected</div>
            <div class="kpi-value">{len(insights.key_drivers)}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Core Insights</div>
            <div class="kpi-value">{len(insights.insights)}</div>
        </div>
    </div>

    <div class="charts-grid">
        {"".join(f'<div class="chart-box">{div}</div>' for div in chart_divs)}
    </div>

    <div class="footer">
        Automated by <strong>Agentic Data Storyteller</strong> | Created by Nitesh Beniwal
    </div>
</body>
</html>"""

        os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_html_path

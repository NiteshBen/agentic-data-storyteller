import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from ..models.schema import DatasetProfile, InsightItem, InsightReport

class InsightDiscoveryAgent:
    """
    Autonomous agent that detects high-impact business drivers,
    statistical anomalies, categorical leaders, and growth trajectories.
    """

    def __init__(self, name: str = "InsightDiscoveryAgent"):
        self.name = name

    def discover(self, df: pd.DataFrame, profile: DatasetProfile) -> InsightReport:
        insights: List[InsightItem] = []
        top_categories: Dict[str, List[Dict[str, Any]]] = {}
        key_drivers: List[Dict[str, Any]] = []

        # 1. Driver discovery via Correlation Analysis
        seen_pairs = set()
        for col_a, row_data in profile.correlations.items():
            for col_b, r_val in row_data.items():
                if col_a != col_b and (col_b, col_a) not in seen_pairs:
                    seen_pairs.add((col_a, col_b))
                    if abs(r_val) >= 0.45:
                        direction = "positive" if r_val > 0 else "negative"
                        key_drivers.append({
                            "feature_a": col_a,
                            "feature_b": col_b,
                            "correlation": r_val,
                            "direction": direction
                        })
                        insights.append(InsightItem(
                            category="driver",
                            title=f"Significant {direction.title()} Relationship: {col_a} & {col_b}",
                            description=f"Observed correlation of {r_val:.2f}. Changes in {col_a} strongly track variations in {col_b}.",
                            importance=round(min(1.0, abs(r_val)), 2),
                            metrics={"r": r_val, "col_a": col_a, "col_b": col_b}
                        ))

        # 2. Outlier / Anomaly Detection Insights
        total_outliers = sum(profile.outliers_iqr.values())
        if total_outliers > 0:
            top_outlier_col = max(profile.outliers_iqr, key=profile.outliers_iqr.get)
            count = profile.outliers_iqr[top_outlier_col]
            pct = round((count / profile.row_count) * 100, 1) if profile.row_count > 0 else 0
            if count > 0:
                insights.append(InsightItem(
                    category="anomaly",
                    title=f"Extreme Variance Detected in '{top_outlier_col}'",
                    description=f"{count} records ({pct}% of dataset) exceed 1.5x IQR boundaries, representing high-leverage outliers or special cases.",
                    importance=0.85,
                    metrics={"column": top_outlier_col, "outlier_count": count, "outlier_pct": pct}
                ))

        # 3. Categorical Leaders & Concentration Insights
        for cat_col in profile.categorical_columns:
            val_counts = df[cat_col].value_counts(normalize=True) * 100
            top_val = val_counts.index[0]
            top_share = round(float(val_counts.iloc[0]), 1)
            
            # Store summary distribution
            counts_raw = df[cat_col].value_counts().head(5).to_dict()
            top_categories[cat_col] = [{"name": str(k), "count": int(v)} for k, v in counts_raw.items()]

            if top_share >= 35.0:
                insights.append(InsightItem(
                    category="distribution",
                    title=f"Market Concentration in '{cat_col}': {top_val}",
                    description=f"The top category '{top_val}' accounts for {top_share}% of all activity across {profile.row_count:,} records.",
                    importance=0.75,
                    metrics={"column": cat_col, "top_category": top_val, "share_pct": top_share}
                ))

        # 4. Temporal Trend Analysis (if datetime exists)
        date_trends = None
        if profile.datetime_columns:
            dt_col = profile.datetime_columns[0]
            try:
                temp_df = df.copy()
                temp_df["_parsed_dt"] = pd.to_datetime(temp_df[dt_col], errors="coerce")
                temp_df = temp_df.dropna(subset=["_parsed_dt"]).sort_values("_parsed_dt")
                
                # Monthly aggregation
                monthly = temp_df.set_index("_parsed_dt").resample("ME").size()
                if len(monthly) >= 2:
                    first_month = int(monthly.iloc[0])
                    last_month = int(monthly.iloc[-1])
                    growth_rate = round(((last_month - first_month) / max(1, first_month)) * 100, 1)
                    date_trends = {
                        "date_column": dt_col,
                        "start_date": str(temp_df["_parsed_dt"].min().date()),
                        "end_date": str(temp_df["_parsed_dt"].max().date()),
                        "periods": len(monthly),
                        "growth_rate_pct": growth_rate
                    }
                    insights.append(InsightItem(
                        category="trend",
                        title=f"Temporal Trajectory ({date_trends['start_date']} to {date_trends['end_date']})",
                        description=f"Observed volume trend shows a {growth_rate:+}% shift over the monitored period.",
                        importance=0.88,
                        metrics=date_trends
                    ))
            except Exception:
                pass

        # Sort insights by importance descending
        insights.sort(key=lambda x: x.importance, reverse=True)

        summary = (
            f"Analyzed {profile.row_count:,} records across {profile.column_count} dimensions. "
            f"Discovered {len(insights)} primary insights, {len(key_drivers)} key driver correlations, "
            f"and mapped categorical dominance across {len(profile.categorical_columns)} dimensions."
        )

        return InsightReport(
            summary=summary,
            insights=insights,
            top_categories=top_categories,
            key_drivers=key_drivers,
            date_trends=date_trends
        )

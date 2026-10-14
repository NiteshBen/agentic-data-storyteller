from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class ColumnProfile:
    name: str
    dtype: str
    missing_count: int
    missing_pct: float
    unique_count: int
    sample_values: List[Any]
    is_numeric: bool
    is_categorical: bool
    is_datetime: bool
    stats: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DatasetProfile:
    row_count: int
    column_count: int
    columns: Dict[str, ColumnProfile]
    numeric_columns: List[str]
    categorical_columns: List[str]
    datetime_columns: List[str]
    memory_usage_kb: float
    correlations: Dict[str, Dict[str, float]] = field(default_factory=dict)
    outliers_iqr: Dict[str, int] = field(default_factory=dict)

@dataclass
class InsightItem:
    category: str  # "driver", "anomaly", "trend", "distribution"
    title: str
    description: str
    importance: float  # 0.0 - 1.0
    metrics: Dict[str, Any] = field(default_factory=dict)

@dataclass
class InsightReport:
    summary: str
    insights: List[InsightItem]
    top_categories: Dict[str, List[Dict[str, Any]]]
    key_drivers: List[Dict[str, Any]]
    date_trends: Optional[Dict[str, Any]] = None

@dataclass
class StoryOutput:
    executive_summary: str
    executive_story_markdown: str
    linkedin_post: str
    html_dashboard_path: str
    infographic_svg_path: str
    key_metrics: Dict[str, Any]

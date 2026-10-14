import pandas as pd
import numpy as np
from typing import Dict, Any, List
from ..models.schema import ColumnProfile, DatasetProfile

class DataProfilerAgent:
    """
    Autonomous agent responsible for deep statistical profiling,
    schema type inference, distribution calculation, and anomaly detection.
    """
    
    def __init__(self, name: str = "DataProfilerAgent"):
        self.name = name

    def profile(self, df: pd.DataFrame) -> DatasetProfile:
        row_count = len(df)
        column_count = len(df.columns)
        memory_usage_kb = round(df.memory_usage(deep=True).sum() / 1024, 2)
        
        columns_profile: Dict[str, ColumnProfile] = {}
        numeric_cols: List[str] = []
        cat_cols: List[str] = []
        dt_cols: List[str] = []
        outliers: Dict[str, int] = {}
        
        # Analyze each column
        for col in df.columns:
            s = df[col]
            missing_count = int(s.isna().sum())
            missing_pct = round((missing_count / row_count) * 100, 2) if row_count > 0 else 0.0
            unique_count = int(s.nunique())
            
            # Type heuristics
            is_dt = False
            if pd.api.types.is_datetime64_any_dtype(s):
                is_dt = True
            elif s.dtype == object and unique_count > 0:
                # Try parsing date strings if looks like date
                sample_str = str(s.dropna().iloc[0]) if not s.dropna().empty else ""
                if len(sample_str) in [10, 19] and ("-" in sample_str or "/" in sample_str):
                    try:
                        pd.to_datetime(s.dropna().iloc[:20])
                        is_dt = True
                    except Exception:
                        is_dt = False

            is_num = bool(pd.api.types.is_numeric_dtype(s) and not is_dt)
            is_cat = bool(not is_num and not is_dt)
            
            stats: Dict[str, Any] = {}
            if is_num:
                numeric_cols.append(col)
                clean_num = s.dropna()
                if not clean_num.empty:
                    mean_val = float(clean_num.mean())
                    std_val = float(clean_num.std()) if len(clean_num) > 1 else 0.0
                    min_val = float(clean_num.min())
                    max_val = float(clean_num.max())
                    q25 = float(clean_num.quantile(0.25))
                    q50 = float(clean_num.median())
                    q75 = float(clean_num.quantile(0.75))
                    iqr = q75 - q25
                    lower_bound = q25 - (1.5 * iqr)
                    upper_bound = q75 + (1.5 * iqr)
                    outlier_count = int(((clean_num < lower_bound) | (clean_num > upper_bound)).sum())
                    outliers[col] = outlier_count
                    
                    stats = {
                        "mean": round(mean_val, 2),
                        "std": round(std_val, 2),
                        "min": round(min_val, 2),
                        "q25": round(q25, 2),
                        "median": round(q50, 2),
                        "q75": round(q75, 2),
                        "max": round(max_val, 2),
                        "iqr": round(iqr, 2),
                        "outlier_count": outlier_count
                    }
            elif is_dt:
                dt_cols.append(col)
                clean_dt = pd.to_datetime(s.dropna(), errors="coerce")
                if not clean_dt.empty:
                    stats = {
                        "min_date": str(clean_dt.min().date()),
                        "max_date": str(clean_dt.max().date()),
                        "date_span_days": (clean_dt.max() - clean_dt.min()).days
                    }
            else:
                cat_cols.append(col)
                top_counts = s.value_counts().head(5).to_dict()
                stats = {
                    "top_values": {str(k): int(v) for k, v in top_counts.items()}
                }

            sample_vals = [val if pd.notna(val) else None for val in s.head(3).tolist()]
            columns_profile[col] = ColumnProfile(
                name=col,
                dtype=str(s.dtype),
                missing_count=missing_count,
                missing_pct=missing_pct,
                unique_count=unique_count,
                sample_values=sample_vals,
                is_numeric=is_num,
                is_categorical=is_cat,
                is_datetime=is_dt,
                stats=stats
            )
            
        # Pearson correlations
        correlations: Dict[str, Dict[str, float]] = {}
        if len(numeric_cols) >= 2:
            corr_df = df[numeric_cols].corr()
            for r_col in corr_df.index:
                correlations[r_col] = {}
                for c_col in corr_df.columns:
                    val = corr_df.loc[r_col, c_col]
                    correlations[r_col][c_col] = round(float(val), 3) if pd.notna(val) else 0.0

        return DatasetProfile(
            row_count=row_count,
            column_count=column_count,
            columns=columns_profile,
            numeric_columns=numeric_cols,
            categorical_columns=cat_cols,
            datetime_columns=dt_cols,
            memory_usage_kb=memory_usage_kb,
            correlations=correlations,
            outliers_iqr=outliers
        )

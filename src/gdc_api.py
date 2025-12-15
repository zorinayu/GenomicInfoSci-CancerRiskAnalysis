from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd

try:
    import requests
except ImportError as e:  # pragma: no cover
    requests = None  # type: ignore


GDC_BASE_URL = "https://api.gdc.cancer.gov"


@dataclass(frozen=True)
class GdcSampleTypeCounts:
    project_id: str
    primary_tumor: int
    solid_tissue_normal: int
    blood_derived_normal: int
    metastatic: int
    recurrent_tumor: int

    @property
    def tumor_to_solid_normal_ratio(self) -> float:
        return self.primary_tumor / self.solid_tissue_normal if self.solid_tissue_normal else float("nan")


def _require_requests() -> None:
    if requests is None:  # pragma: no cover
        raise ImportError(
            "The 'requests' package is required for GDC API queries. Install it via pip (e.g., pip install requests)."
        )


def gdc_cases_sample_type_facets(project_id: str, timeout_s: int = 60) -> Dict[str, int]:
    """
    Query the GDC /cases endpoint and return counts for samples.sample_type buckets for the given project.

    Notes:
    - The GDC API exposes sample types (e.g., 'primary tumor', 'solid tissue normal') in lower-case keys.
    - Counts are aggregated over sample records linked to cases for the project.
    """
    _require_requests()

    url = f"{GDC_BASE_URL}/cases"
    filters = {
        "op": "and",
        "content": [
            {"op": "in", "content": {"field": "project.project_id", "value": [project_id]}},
        ],
    }
    params = {
        "filters": json.dumps(filters),
        "size": "0",
        "facets": "samples.sample_type",
    }
    resp = requests.get(url, params=params, timeout=timeout_s)
    resp.raise_for_status()
    js = resp.json()
    buckets = js["data"]["aggregations"]["samples.sample_type"]["buckets"]
    return {b["key"]: int(b["doc_count"]) for b in buckets}


def tcga_tumor_vs_normal_counts(
    project_ids: Iterable[str],
    cache_csv: Optional[str | Path] = None,
    refresh: bool = False,
    timeout_s: int = 60,
) -> pd.DataFrame:
    """
    Build a tumor-vs-non-tumor (normal) sample-type count table for TCGA projects via the GDC API.

    - Tumor: 'primary tumor'
    - Non-tumor (normal): 'solid tissue normal'
    Also reports 'blood derived normal', 'metastatic', and 'recurrent tumor' if present.

    If cache_csv is provided and exists, it is loaded unless refresh=True.
    """
    cache_path = Path(cache_csv) if cache_csv is not None else None
    if cache_path and cache_path.exists() and not refresh:
        return pd.read_csv(cache_path)

    rows: List[Dict[str, object]] = []
    for pid in project_ids:
        counts = gdc_cases_sample_type_facets(pid, timeout_s=timeout_s)
        row = GdcSampleTypeCounts(
            project_id=pid,
            primary_tumor=counts.get("primary tumor", 0),
            solid_tissue_normal=counts.get("solid tissue normal", 0),
            blood_derived_normal=counts.get("blood derived normal", 0),
            metastatic=counts.get("metastatic", 0),
            recurrent_tumor=counts.get("recurrent tumor", 0),
        )
        rows.append(
            {
                "project_id": row.project_id,
                "primary_tumor": row.primary_tumor,
                "solid_tissue_normal": row.solid_tissue_normal,
                "blood_derived_normal": row.blood_derived_normal,
                "metastatic": row.metastatic,
                "recurrent_tumor": row.recurrent_tumor,
                "tumor_to_solid_normal_ratio": row.tumor_to_solid_normal_ratio,
            }
        )

    df = pd.DataFrame(rows)
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cache_path, index=False)
    return df



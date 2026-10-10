"""
Backend Google Ads Export Engine.
Generates production-grade CSV files ready for Google Ads Editor import,
including Promoted Keywords, Negative Match Lists, and Comprehensive Audit Trails.
"""

from triage_engine.exporter import (
    export_triage_results,
)

__all__ = [
    "export_triage_results",
]

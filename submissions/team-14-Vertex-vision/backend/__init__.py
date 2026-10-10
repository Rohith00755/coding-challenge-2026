"""
Backend Core Package for TriageIQ (PS-01 Search Term Triage Engine).
Provides statistical bounds, business rule evaluation, semantic intent clustering,
negative keyword extraction, audit export, and AI Copilot diagnostics.
"""

from triage_engine.rules import (
    TriageEngine,
    AdvertiserProfile
)
from triage_engine.stats import (
    wilson_score_interval,
    empirical_bayes_cvr,
    calculate_derived_metrics,
    calculate_uncertainty_metrics
)
from triage_engine.clustering import cluster_search_queries
from triage_engine.copilot import generate_copilot_response
from triage_engine.negatives import generate_context_aware_negative_suggestions
from triage_engine.learning import ReviewerPrecedentMemory
from triage_engine.exporter import export_triage_results

__all__ = [
    "TriageEngine",
    "AdvertiserProfile",
    "wilson_score_interval",
    "empirical_bayes_cvr",
    "calculate_derived_metrics",
    "calculate_uncertainty_metrics",
    "cluster_search_queries",
    "generate_copilot_response",
    "generate_context_aware_negative_suggestions",
    "ReviewerPrecedentMemory",
    "export_triage_results",
]

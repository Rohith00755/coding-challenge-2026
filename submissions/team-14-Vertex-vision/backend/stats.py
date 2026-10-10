"""
Backend Statistical Engine.
Implements Wilson Score Confidence Intervals, Empirical Bayes Shrinkage,
and uncertainty-aware marketing metrics.
"""

from triage_engine.stats import (
    wilson_score_interval,
    empirical_bayes_cvr,
    calculate_derived_metrics,
    calculate_uncertainty_metrics,
)

__all__ = [
    "wilson_score_interval",
    "empirical_bayes_cvr",
    "calculate_derived_metrics",
    "calculate_uncertainty_metrics",
]

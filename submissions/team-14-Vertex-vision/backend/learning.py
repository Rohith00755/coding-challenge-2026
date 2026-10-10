"""
Backend Active Learning & Precedent Memory.
Stores and matches human reviewer overrides using Levenshtein edit distance and token overlap
to guide future automated triage decisions.
"""

from triage_engine.learning import (
    ReviewerPrecedentMemory,
    compute_query_similarity,
    tokenize_query,
)

__all__ = [
    "ReviewerPrecedentMemory",
    "compute_query_similarity",
    "tokenize_query",
]

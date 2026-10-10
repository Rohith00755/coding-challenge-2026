"""
Backend Intent Clustering Engine.
Groups semantically similar queries and variations using TF-IDF tokenization and character n-grams.
"""

from triage_engine.clustering import cluster_search_queries

__all__ = [
    "cluster_search_queries",
]

"""
Hierarchical digest processing module.

EXPERIMENTAL — NOT active in the production pipeline (run.py).

This module implements a two-stage LLM pipeline (per-thread summarization →
final aggregation) designed for high email volumes. It is kept for future
exploration but is NOT used by the current pipeline because:

  1. It violates ADR-002 (single LLM call per run).
  2. Multiple concurrent LLM calls would exhaust the 15 RPM gateway limit.
  3. It depends on the EnhancedDigest v2 schema which is not yet integrated.

Integration path: requires relaxed rate limits (≥60 RPM) or a separate
queue, and explicit opt-in via a CLI flag (e.g. --hierarchical).
Until then, all production runs use the standard single-call path in run.py.
"""

from .processor import HierarchicalProcessor
from .metrics import HierarchicalMetrics

__all__ = ["HierarchicalProcessor", "HierarchicalMetrics"]

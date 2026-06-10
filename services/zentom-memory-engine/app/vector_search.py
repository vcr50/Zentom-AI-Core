"""
Zentom Memory Engine — Vector Search

Semantic search over incident memories using text similarity.
Supports:
  - TF-IDF based text similarity (no external ML deps required)
  - pgvector integration for production (PostgreSQL + vector extension)
  - Fallback keyword matching for simple queries

In production, replace with proper embedding model (sentence-transformers)
and pgvector for high-quality semantic search.
"""

import math
import re
from collections import Counter
from typing import Optional
from .memory_store import MemoryStore, get_store


def _tokenize(text: str) -> list[str]:
    """Simple tokenization: lowercase, split on non-alphanumeric, remove short tokens."""
    if not text:
        return []
    text = text.lower()
    tokens = re.findall(r'[a-z0-9]{2,}', text)
    return tokens


def _compute_tf(tokens: list[str]) -> dict[str, float]:
    """Compute term frequency for a list of tokens."""
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = len(tokens)
    return {term: count / total for term, count in counts.items()}


def _compute_idf(documents: list[list[str]]) -> dict[str, float]:
    """Compute inverse document frequency across all documents."""
    n_docs = len(documents)
    if n_docs == 0:
        return {}
    doc_freq = Counter()
    for doc_tokens in documents:
        unique_terms = set(doc_tokens)
        for term in unique_terms:
            doc_freq[term] += 1
    return {
        term: math.log((n_docs + 1) / (freq + 1)) + 1
        for term, freq in doc_freq.items()
    }


def _cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """Compute cosine similarity between two sparse vectors."""
    all_terms = set(vec_a.keys()) | set(vec_b.keys())
    if not all_terms:
        return 0.0

    dot_product = sum(vec_a.get(t, 0) * vec_b.get(t, 0) for t in all_terms)
    norm_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    norm_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


class VectorSearch:
    """
    Text-based similarity search over memory entries.

    Uses TF-IDF for similarity scoring. In production, replace with
    proper vector embeddings + pgvector for semantic search.
    """

    def __init__(self, store: MemoryStore | None = None):
        self.store = store or get_store()

    def find_similar(
        self,
        query: str,
        incident_type: str | None = None,
        limit: int = 10,
        min_similarity: float = 0.1,
    ) -> list[dict]:
        """
        Find memory entries similar to the query text.

        Args:
            query: Search query text
            incident_type: Optional filter by incident type
            limit: Maximum results to return
            min_similarity: Minimum similarity threshold (0-1)

        Returns:
            List of dicts with 'entry' and 'similarity' keys
        """
        # Get all searchable entries
        entries = self.store.search(incident_type=incident_type, limit=500)

        if not entries:
            return []

        # Tokenize query
        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        # Build document corpus for IDF
        all_docs = [query_tokens]
        entry_tokens_map = {}
        for entry in entries:
            # Combine searchable text fields
            text_parts = [
                entry.get("embedding_text", ""),
                entry.get("summary", ""),
                entry.get("root_cause", ""),
                entry.get("recommended_action", ""),
                entry.get("title", ""),
            ]
            text = " ".join(part for part in text_parts if part)
            tokens = _tokenize(text)
            if tokens:
                all_docs.append(tokens)
                entry_tokens_map[entry.get("id")] = (entry, tokens)

        # Compute IDF
        idf = _compute_idf(all_docs)

        # Compute TF-IDF for query
        query_tf = _compute_tf(query_tokens)
        query_tfidf = {term: tf * idf.get(term, 1.0) for term, tf in query_tf.items()}

        # Score each entry
        results = []
        for entry_id, (entry, tokens) in entry_tokens_map.items():
            entry_tf = _compute_tf(tokens)
            entry_tfidf = {term: tf * idf.get(term, 1.0) for term, tf in entry_tf.items()}

            similarity = _cosine_similarity(query_tfidf, entry_tfidf)

            if similarity >= min_similarity:
                results.append({
                    "entry": entry,
                    "similarity": round(similarity, 4),
                })

        # Sort by similarity descending
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:limit]

    def find_by_keywords(
        self,
        keywords: list[str],
        incident_type: str | None = None,
        limit: int = 10,
    ) -> list[dict]:
        """
        Simple keyword-based search. Matches entries containing any of the keywords.

        Returns entries ranked by number of keyword matches.
        """
        entries = self.store.search(incident_type=incident_type, limit=500)
        keywords_lower = [kw.lower() for kw in keywords]

        results = []
        for entry in entries:
            # Combine searchable text
            text = " ".join([
                entry.get("embedding_text", ""),
                entry.get("summary", ""),
                entry.get("root_cause", ""),
                entry.get("recommended_action", ""),
                entry.get("title", ""),
            ]).lower()

            matches = sum(1 for kw in keywords_lower if kw in text)
            if matches > 0:
                results.append({
                    "entry": entry,
                    "keyword_matches": matches,
                    "matched_keywords": [kw for kw in keywords_lower if kw in text],
                })

        results.sort(key=lambda x: x["keyword_matches"], reverse=True)
        return results[:limit]


# Global search instance
_search: VectorSearch | None = None


def get_search(store: MemoryStore | None = None) -> VectorSearch:
    """Get or create the global VectorSearch instance."""
    global _search
    if _search is None:
        _search = VectorSearch(store)
    return _search


def find_similar_incidents(query: str, limit: int = 10) -> list[dict]:
    """
    Find similar incidents by query text.

    Backward-compatible function.
    """
    search = get_search()
    results = search.find_similar(query, limit=limit)
    return results


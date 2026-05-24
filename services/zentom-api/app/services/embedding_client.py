import logging

import requests

from app.config import settings


logger = logging.getLogger(__name__)

EMBEDDING_DIMENSIONS = 384


def generate_embedding(text: str) -> list[float] | None:
    """Generate a 384-dim embedding vector from text using Ollama all-minilm.

    Returns None on any failure so callers can fall back gracefully.
    """
    if not text or not text.strip():
        return None

    url = f"{settings.LOCAL_LLM_URL}/api/embeddings"
    payload = {
        "model": settings.EMBEDDING_MODEL,
        "prompt": text.strip(),
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()

        embedding = data.get("embedding")
        if not embedding or not isinstance(embedding, list):
            logger.warning("Ollama returned empty or invalid embedding.")
            return None

        if len(embedding) != EMBEDDING_DIMENSIONS:
            logger.warning(
                "Embedding dimension mismatch: expected %d, got %d",
                EMBEDDING_DIMENSIONS,
                len(embedding),
            )
            return None

        return embedding

    except requests.exceptions.ConnectionError:
        logger.warning("Cannot connect to Ollama at %s for embeddings.", url)
        return None
    except requests.exceptions.Timeout:
        logger.warning("Ollama embedding request timed out.")
        return None
    except Exception as exc:
        logger.warning("Embedding generation failed: %s", exc)
        return None

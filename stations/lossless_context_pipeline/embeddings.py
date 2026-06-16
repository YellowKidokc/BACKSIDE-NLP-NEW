from __future__ import annotations

from pathlib import Path


class Embedder:
    def __init__(self, mode: str = "none", model_path: str = "X:/Backside/_models/downloaded/sbert_minilm") -> None:
        self.mode = mode
        self.model_path = model_path
        self._model = None

    def embed(self, text: str) -> list[float] | None:
        if self.mode == "none":
            return None
        if self.mode != "sbert":
            raise ValueError(f"Unknown embedding mode: {self.mode}")
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            path = Path(self.model_path)
            self._model = SentenceTransformer(str(path if path.exists() else self.model_path))
        vector = self._model.encode(text, normalize_embeddings=True)
        return [float(item) for item in vector.tolist()]

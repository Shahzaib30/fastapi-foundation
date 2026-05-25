from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import joblib
import torch
import torch.nn as nn

from app.core.config import PROJECT_MODEL_FILE, SPAM_MODEL_FILE, SPAM_VOCAB_FILE


class SpamDetector(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int = 50) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.fc = nn.Linear(embed_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embedding(x).mean(dim=1)
        return self.sigmoid(self.fc(x))


@dataclass
class ProjectClassifierService:
    model_path: str = str(PROJECT_MODEL_FILE)

    def load(self):
        return joblib.load(self.model_path)

    def predict(self, description: str):
        model = self.load()
        prediction = model.predict([description])[0]
        confidence = None
        if hasattr(model, "predict_proba"):
            confidence = float(max(model.predict_proba([description])[0]))
        return {"project_type": prediction, "confidence": confidence}


@dataclass
class SpamClassificationService:
    model_path: str = str(SPAM_MODEL_FILE)
    vocab_path: str = str(SPAM_VOCAB_FILE)

    def load_vocab(self) -> Dict[str, int]:
        return joblib.load(self.vocab_path)

    def load_model(self, vocab_size: int) -> SpamDetector:
        model = SpamDetector(vocab_size)
        state_dict = torch.load(self.model_path, map_location="cpu")
        model.load_state_dict(state_dict)
        model.eval()
        return model

    def text_to_tensor(self, text: str, vocab: Dict[str, int]) -> torch.Tensor:
        indices = [vocab.get(word, vocab["<UNK>"]) for word in text.lower().split()]
        return torch.tensor([indices], dtype=torch.long)

    def predict(self, message: str):
        vocab = self.load_vocab()
        model = self.load_model(len(vocab))
        tensor = self.text_to_tensor(message, vocab)
        with torch.no_grad():
            score = float(model(tensor).item())
        prediction = "spam" if score > 0.5 else "ham"
        return {"prediction": prediction, "score": score}

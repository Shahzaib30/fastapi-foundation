from __future__ import annotations

import joblib
import pandas as pd
import torch
import torch.nn as nn


def build_vocab(texts):
    vocab = {"<PAD>": 0, "<UNK>": 1}
    for text in texts:
        for word in text.split():
            if word not in vocab:
                vocab[word] = len(vocab)
    return vocab


class SpamDetector(nn.Module):
    def __init__(self, vocab_size, embed_dim=50):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.fc = nn.Linear(embed_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.embedding(x).mean(dim=1)
        return self.sigmoid(self.fc(x))


def main() -> None:
    df = pd.read_csv("spam.csv", encoding="latin-1")
    vocab = build_vocab(df["v2"].tolist())
    print("Vocabulary built with size:", len(vocab), "Sample:", list(vocab.items())[:10])

    model = SpamDetector(len(vocab))
    torch.save(model.state_dict(), "spam_detector.pth")
    joblib.dump(vocab, "vocab.pkl")
    print("Model and vocabulary saved successfully")


if __name__ == "__main__":
    main()

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import log
import re

TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


@dataclass(frozen=True)
class Document:
    id: str
    text: str
    title: str = ""


@dataclass(frozen=True)
class Result:
    id: str
    score: float
    title: str
    snippet: str


class Index:
    def __init__(self, documents: list[Document], k1: float = 1.5, b: float = 0.75):
        if not documents:
            raise ValueError("at least one document is required")
        self.documents, self.k1, self.b = documents, k1, b
        self.tokens = [tokenize(doc.title + " " + doc.text) for doc in documents]
        self.freqs = [Counter(row) for row in self.tokens]
        self.avgdl = sum(map(len, self.tokens)) / len(self.tokens)
        self.df = Counter(term for row in self.freqs for term in row)

    def search(self, query: str, top_k: int = 10) -> list[Result]:
        terms = tokenize(query)
        ranked = []
        for doc, tokens, freq in zip(self.documents, self.tokens, self.freqs):
            score = 0.0
            for term in terms:
                tf = freq[term]
                if not tf:
                    continue
                idf = log(1 + (len(self.documents) - self.df[term] + 0.5) / (self.df[term] + 0.5))
                score += idf * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * len(tokens) / self.avgdl))
            if score:
                snippet = self._snippet(doc.text, terms)
                ranked.append(Result(doc.id, score, doc.title, snippet))
        return sorted(ranked, key=lambda item: (-item.score, item.id))[:top_k]

    @staticmethod
    def _snippet(text: str, terms: list[str], width: int = 180) -> str:
        lower = text.lower()
        positions = [lower.find(term) for term in terms if lower.find(term) >= 0]
        start = max(0, (min(positions) if positions else 0) - width // 3)
        return " ".join(text[start:start + width].split())


# BM25 Document Search

The Colab `Indexer` and `SearchAgent` experiment rebuilt as a small, typed search library. It provides deterministic tokenization, Okapi BM25 scoring, snippets, and a JSONL CLI.

```bash
pip install -e .[dev]
pytest
bm25-search documents.jsonl "your query"
```

Each JSONL document needs `id` and `text`; `title` is optional.


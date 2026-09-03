import argparse
import json
from .index import Document, Index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("documents")
    parser.add_argument("query")
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()
    with open(args.documents, encoding="utf-8") as handle:
        documents = [Document(**json.loads(line)) for line in handle if line.strip()]
    for result in Index(documents).search(args.query, args.top_k):
        print(json.dumps(result.__dict__))


if __name__ == "__main__":
    main()


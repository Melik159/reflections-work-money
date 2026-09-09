"""Read-only retrieval over one explicitly selected provenance collection."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from rag.iterative import search  # noqa: E402

COLLECTIONS = ("SOURCE_CORPUS", "DERIVED_ANALYSIS", "EXTERNAL_LITERATURE")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", choices=COLLECTIONS, required=True)
    parser.add_argument("--level", choices=("SECTION", "PAGE", "PARAGRAPH", "CLAIM_WINDOW"))
    parser.add_argument("-k", type=int, default=5)
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    if args.k < 1 or not args.query.strip():
        parser.error("-k must be positive and --query must contain text")
    path = ROOT / ("research_state/iteration001/external_literature_index.json"
                   if args.collection == "EXTERNAL_LITERATURE" else "rag/index/iterative.json")
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        parser.error(f"Cannot read index {path}: {exc}. No index was rebuilt.")
    if not isinstance(data, dict) or not isinstance(data.get("rows"), list):
        parser.error(f"Invalid index schema in {path}: expected mapping with rows list")
    rows = [row for row in data["rows"] if row.get("collection") == args.collection]
    if args.level:
        rows = [row for row in rows if row.get("level") == args.level]
    elif args.collection == "SOURCE_CORPUS":
        rows = [row for row in rows if row.get("level") in {"PAGE", "SECTION"}]
    if not rows:
        parser.error(f"No indexed rows for {args.collection}, level={args.level or 'default'}; no fallback to another collection")
    required = {"document", "page", "section", "chunk", "chunk_id", "text", "source_type"}
    for row in rows:
        missing = required - row.keys()
        if missing or row["source_type"] != args.collection:
            parser.error(f"Invalid provenance metadata: missing={sorted(missing)}, source_type={row.get('source_type')}")
    for result in search(rows, args.query, method="bm25", k=args.k):
        if result.get("collection") != args.collection or result.get("source_type") != args.collection:
            parser.error("Retrieval provenance mismatch; output refused")
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

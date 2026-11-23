"""Command line entry point for first-stage ingestion."""
import argparse
from pathlib import Path
import json

from .metadata import load_sources
from .pipeline import ingest_sources


def main() -> int:
    parser = argparse.ArgumentParser(description="擷取並清理官方 NFC 公開來源")
    parser.add_argument("--sources", type=Path, default=Path("data/sources.json"))
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    args = parser.parse_args()
    sources = load_sources(args.sources)
    report = ingest_sources(sources, args.data_dir)
    print(json.dumps(report["summary"] | {"run_id": report["run_id"]}, ensure_ascii=False, indent=2))
    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

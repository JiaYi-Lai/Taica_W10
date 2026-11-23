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
    parser.add_argument("--source-id", required=True, help="一次只擷取一份來源，例如 S05")
    args = parser.parse_args()
    sources = load_sources(args.sources)
    selected = [source for source in sources if source.source_id == args.source_id]
    if not selected:
        parser.error(f"來源 Registry 找不到 source_id={args.source_id}")
    report = ingest_sources(selected, args.data_dir, registry_sources=sources)
    print(json.dumps(report["summary"] | {"run_id": report["run_id"]}, ensure_ascii=False, indent=2))
    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

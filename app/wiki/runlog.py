"""Append-only human and structured records for Wiki operations."""
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid


def record_wiki_operation(*, operation: str, status: str, input_refs: list[str],
                          output_refs: list[str], validation: dict,
                          project_dir: Path = Path("."), details: dict | None = None,
                          started_at: str | None = None) -> dict:
    project_dir = project_dir.resolve()
    run_id = str(uuid.uuid4())
    ended = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    started = started_at or ended
    runs_dir = project_dir / "data" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    run = {"run_id": run_id, "operation": operation, "started_at": started,
           "ended_at": ended, "status": status,
           "input_refs": input_refs, "output_refs": output_refs,
           "validation": validation, "details": details or {}}
    run_path = runs_dir / f"{run_id}.json"
    run_path.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log_path = project_dir / "wiki" / "log.md"
    with log_path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(f"\n## [{ended}] {operation} | {run_id}\n")
        stream.write(f"- Run ID: `{run_id}`\n")
        stream.write(f"- Inputs: {', '.join(input_refs) if input_refs else 'none'}\n")
        stream.write(f"- Outputs: {', '.join(output_refs) if output_refs else 'none'}\n")
        stream.write(f"- Validation: {status}; {json.dumps(validation, ensure_ascii=False)}\n")
        if details:
            stream.write(f"- Notes: {json.dumps(details, ensure_ascii=False)}\n")
    return {**run, "run_path": run_path.relative_to(project_dir).as_posix()}

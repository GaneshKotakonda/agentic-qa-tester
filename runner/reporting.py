
import json
import uuid

from datetime import datetime, timezone
from pathlib import Path


def create_run_dir():
    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S"
    )

    run_id = f"{timestamp}_{uuid.uuid4().hex[:8]}"

    run_dir = Path("artifacts") / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    return run_id, run_dir


def save_report(run_dir, report):
    report_path = run_dir / "result.json"

    report_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    return report_path

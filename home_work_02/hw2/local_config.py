"""The untracked packaging configuration (BR-03).

The real student id lives only in ``home_work_02/.local/packaging.json`` (ignored by git) and in
the names of the submitted files. Tracked files always write the placeholder ``<學號>``. Callers
must not print the value, log it, or write it into any tracked file.
"""
import json
import re
from pathlib import Path

from .paths import PACKAGING_CONFIG

PLACEHOLDER = "<學號>"
_STUDENT_ID = re.compile(r"^[0-9A-Za-z]{6,16}$")


class LocalConfigError(RuntimeError):
    """The packaging configuration is missing or malformed (the message never contains the id)."""


def read_student_id(path: Path = PACKAGING_CONFIG) -> str:
    """The student id from the untracked packaging configuration.

    Raises LocalConfigError when the file is missing, is not a JSON object with a
    ``student_id`` string, or the value is not 6-16 letters or digits.
    """
    path = Path(path)
    if not path.is_file():
        raise LocalConfigError(
            f"packaging configuration not found: {path} "
            '(create it with {"student_id": "<學號>"}; it is ignored by git)')
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise LocalConfigError(f"packaging configuration is not valid JSON: {path}") from exc
    value = data.get("student_id") if isinstance(data, dict) else None
    if not isinstance(value, str) or not _STUDENT_ID.match(value) or value == PLACEHOLDER:
        raise LocalConfigError(
            f"packaging configuration {path} has no valid student_id (6-16 letters or digits)")
    return value

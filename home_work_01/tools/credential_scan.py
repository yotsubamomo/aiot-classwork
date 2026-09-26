#!/usr/bin/env python3
"""CI credential mechanical checks for ``home_work_01`` (AC-07 b/c/d, decision A-5).

This is the secret gate the Outcome Contract requires GitHub Actions to run on
every push (Spec R-TC-6 / R-SEC-1; high-risk H-1). Without ever printing a secret
value it confirms:

* **(b)** ``git ls-files`` tracks no ``.env`` file -- only ``.env.example`` (which
  holds just the variable name) is allowed to be committed;
* **(c)** no tracked file, and no committed diff anywhere in history, contains a
  string in the CWA key format. The ignored ``home_work_01/.env`` is explicitly
  excluded from the scan (the requirement is "no key in *tracked* content", not
  "empty working tree", so the untracked local key file is never read);
* **(d)** the committed fixtures (including the V2 O-A0001-001 sample) and the
  saved raw forecast JSON carry no non-empty ``Authorization`` value (and no
  key-format string).

Only the offending path and the *kind* of match are ever printed -- never the
matched text -- so the CI log stays free of secrets (H-1). The key / Authorization
patterns are reused from :mod:`ingestion.checks`, so this gate and the offline
test suite (``tests/test_secrets.py``) agree on what a secret looks like.

**Documented example allowlist (AC-07(c) / A-5 interpretation).** Exactly one
key-*format* string is deliberately present in tracked, non-secret content: the
placeholder ``CWA-1234-5678-90ab-cdef`` that ``tests/test_secrets.py`` uses to
prove the detector flags a key (also quoted in two audit records). A real CWA key
is a ``CWA-`` prefixed UUID (8-4-4-4-12 hex); this 4-4-4-4 placeholder can never be
a registered key. It is removed before matching so the scan stays meaningful -- a
real key is still caught in *any* file -- without failing on the project's own
documented example. The worklog for Issue #22 records this interpretation and the
one-off literal-real-key self-verification that this allowlist does not mask a real
leak. :mod:`ingestion.checks` itself is unchanged, so its detector self-test still
proves keys are flagged.

Exit code: ``0`` when every check passes, ``1`` when any finding is present, ``2``
on an environment error (e.g. not inside a git work tree).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from ingestion.checks import AUTH_VALUE_PATTERN, KEY_PATTERN

# The one tracked env file that is allowed (variable name only, no value).
_ALLOWED_ENV_FILE = ".env.example"
# Never read this file's content into the scan: the real key lives only in this
# ignored, untracked file (it is not tracked, so git never lists it; this is a
# belt-and-braces guard so the scan can never open it).
_EXCLUDED_BASENAMES = {".env"}
# AC-07(d): these committed artifacts must carry no Authorization value / key.
# V2 (SPEC-V2 R-V2-SEC-5, AC-V2-17(a); Issue #35): the sanitised real
# O-A0001-001 sample is added. Every tracked file -- including the V2 backend
# code (server.py, api/index.py, observation.py) -- is already covered by (c).
_AUTH_ARTIFACTS = (
    "home_work_01/tests/fixtures/F-D0047-091_sample.json",
    "home_work_01/data/raw/F-D0047-091.json",
    "home_work_01/data/raw/F-D0047-091.meta.json",
    "home_work_01/tests/fixtures/O-A0001-001_sample.json",
    # Issue #40: the sanitised real O-A0058-006 radar metadata sample.
    "home_work_01/tests/fixtures/O-A0058-006_metadata_sample.json",
)
# Documented, deliberately-fake example keys that are NOT secrets (see module
# docstring). Removed before matching so they never trip the scan.
_EXAMPLE_ALLOWLIST = ("CWA-1234-5678-90ab-cdef",)


def _strip_examples(text: str) -> str:
    """Remove documented fake example keys so only real matches remain."""
    for token in _EXAMPLE_ALLOWLIST:
        text = text.replace(token, "")
    return text


def _basename(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def _is_env_file(path: str) -> bool:
    name = _basename(path)
    return name == ".env" or name.startswith(".env.")


def repo_root() -> Path:
    """Return the git work-tree root; raise on failure (handled by ``main``)."""
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return Path(out)


def tracked_files(root: Path) -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    return [p for p in out.split("\0") if p]


def check_env_not_tracked(tracked: list[str]) -> list[str]:
    """(b) No ``.env`` file may be tracked; ``.env.example`` is allowed."""
    findings: list[str] = []
    for path in tracked:
        if _is_env_file(path) and _basename(path) != _ALLOWED_ENV_FILE:
            findings.append(f"(b) tracked env file must not be committed: {path}")
    return findings


def check_tracked_no_key(root: Path, tracked: list[str]) -> list[str]:
    """(c) No tracked file contains a CWA-key-format string."""
    findings: list[str] = []
    for path in tracked:
        if _basename(path) in _EXCLUDED_BASENAMES:
            continue  # never read the ignored local .env
        try:
            data = (root / path).read_bytes()
        except OSError:
            continue
        # Decode leniently: the key pattern is ASCII, so binary noise cannot
        # produce a false 'CWA-...' match, and unreadable bytes are dropped.
        text = _strip_examples(data.decode("utf-8", errors="ignore"))
        if KEY_PATTERN.search(text):
            findings.append(f"(c) tracked file contains a CWA-key-format string: {path}")
    return findings


def check_history_no_key(root: Path) -> list[str]:
    """(c) No committed diff in history contains a CWA-key-format string.

    Streams ``git log -p`` so the whole file is never held in memory. Binary blobs
    are shown by git as 'Binary files differ' (no content), so large binaries are
    not scanned. Requires full history (the CI checkout uses ``fetch-depth: 0``).
    """
    proc = subprocess.Popen(
        ["git", "log", "-p", "--no-color", "--full-history"],
        cwd=root,
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    assert proc.stdout is not None
    hits = 0
    for line in proc.stdout:
        if KEY_PATTERN.search(_strip_examples(line)):
            hits += 1
    proc.stdout.close()
    returncode = proc.wait()
    findings: list[str] = []
    if returncode != 0:
        findings.append(f"(c) 'git log -p' exited {returncode}; history not fully scanned")
    if hits:
        findings.append(
            f"(c) committed history contains {hits} line(s) matching the CWA key pattern"
        )
    return findings


def check_auth_artifacts(root: Path) -> list[str]:
    """(d) Fixture and saved raw JSON carry no Authorization value / key."""
    findings: list[str] = []
    for rel in _AUTH_ARTIFACTS:
        full = root / rel
        if not full.is_file():
            findings.append(f"(d) expected committed artifact is missing: {rel}")
            continue
        text = full.read_text(encoding="utf-8", errors="ignore")
        for match in AUTH_VALUE_PATTERN.finditer(text):
            if match.group("value").strip():
                findings.append(f"(d) non-empty Authorization value present in {rel}")
                break
        if KEY_PATTERN.search(_strip_examples(text)):
            findings.append(f"(d) CWA-key-format string present in {rel}")
    return findings


def run() -> int:
    try:
        root = repo_root()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("error: not inside a git work tree", file=sys.stderr)
        return 2
    tracked = tracked_files(root)
    findings: list[str] = []
    findings += check_env_not_tracked(tracked)
    findings += check_tracked_no_key(root, tracked)
    findings += check_history_no_key(root)
    findings += check_auth_artifacts(root)
    if findings:
        print("CREDENTIAL SCAN FAILED:")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(
        "credential scan passed: "
        f"{len(tracked)} tracked files; no .env tracked (only .env.example); "
        "no CWA-key-format string in tracked files or committed history; "
        "no Authorization value in fixture/raw JSON."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

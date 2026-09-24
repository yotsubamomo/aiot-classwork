"""Unit-local tooling that is not part of the product runtime.

Currently holds the CI credential mechanical checks (``credential_scan``). Kept
out of ``ingestion`` (the product pipeline) so a CI-only utility does not mix
into the graded application code.
"""

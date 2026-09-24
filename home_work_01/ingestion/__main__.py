"""Enable ``python -m ingestion`` to run the pipeline CLI."""

from .pipeline import main

if __name__ == "__main__":
    raise SystemExit(main())

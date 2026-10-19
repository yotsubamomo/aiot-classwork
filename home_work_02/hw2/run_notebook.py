"""Execute hw2.ipynb non-interactively, in place (python -m hw2.run_notebook from home_work_02/)."""
import sys
import time

import nbformat
from nbclient import NotebookClient

from .paths import UNIT_DIR

NOTEBOOK = UNIT_DIR / "hw2.ipynb"


def main() -> int:
    nb = nbformat.read(NOTEBOOK, as_version=4)
    start = time.perf_counter()
    NotebookClient(nb, timeout=3600, kernel_name="python3",
                   resources={"metadata": {"path": str(UNIT_DIR)}}).execute()
    nbformat.write(nb, NOTEBOOK)
    print(f"executed {NOTEBOOK.name} in {time.perf_counter() - start:.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())

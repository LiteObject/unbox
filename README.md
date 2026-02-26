# unbox

A modular CLI tool to extract text content from documents.

## Supported Formats

| Format     | Extension | Library        |
| ---------- | --------- | -------------- |
| PDF        | `.pdf`    | PyMuPDF        |
| PowerPoint | `.pptx`   | python-pptx    |
| Word       | `.docx`   | python-docx    |

## Installation

```bash
pip install -e .
```

For development (includes linting & testing tools):

```bash
pip install -e ".[dev]"
```

## Usage

Extract a single file (creates a `.txt` file alongside the original):

```bash
unbox report.pdf
```

Extract multiple files:

```bash
unbox report.pdf slides.pptx notes.docx
```

Specify an output directory:

```bash
unbox report.pdf --output-dir out/
```

Print to stdout instead of writing files:

```bash
unbox report.pdf --stdout
```

List supported formats:

```bash
unbox --list-formats
```

### Run without installing

You can run unbox as a Python module without installing the console entry point:

```bash
python -m unbox report.pdf
```

Or without any install at all (just the dependencies):

```powershell
# PowerShell
$env:PYTHONPATH = "src"; python -m unbox report.pdf
```

```bash
# Bash
PYTHONPATH=src python -m unbox report.pdf
```

## Adding a New Format

Adding support for a new file format requires **three steps**:

### 1. Create a new extractor module

Create a file in `src/unbox/extractors/`, for example `xlsx.py`:

```python
"""Excel (.xlsx) text extractor."""

from __future__ import annotations

from pathlib import Path

from unbox.base import BaseExtractor


class XlsxExtractor(BaseExtractor):
    """Extract text from Excel spreadsheets."""

    supported_extensions = [".xlsx"]

    def extract(self, file_path: Path) -> str:
        # Your extraction logic here
        ...
```

### 2. Register it

Add one import line to `src/unbox/extractors/__init__.py`:

```python
from unbox.extractors.xlsx import XlsxExtractor
```

### 3. Add the dependency

Add the required library to the `dependencies` list in `pyproject.toml`.

That's it — the new format is automatically available via the CLI.

## Development

```bash
# Lint
ruff check src/ tests/

# Format
ruff format src/ tests/

# Test
pytest tests/ -v
```

## License

MIT

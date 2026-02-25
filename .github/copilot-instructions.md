# Unbox — Project Guidelines

## Code Style

- **Every `.py` file** starts with `from __future__ import annotations` and a module-level docstring.
- Type-hint all function signatures, including `-> None` on test methods.
- Use PEP 604 unions (`X | None`) and `ClassVar` for class-level annotations.
- Docstrings follow **NumPy style** (`Parameters`, `Returns`, `Raises` with `---` underlines).  
  See [src/unbox/base.py](../src/unbox/base.py) for the canonical example.
- Absolute imports only (`from unbox.base import …`), never relative.
- Private helpers prefixed with `_` (e.g. `_build_parser`, `_registry`).
- Ruff enforces rules `E, F, W, I, UP` at line-length 88 targeting Python 3.10+.

## Architecture

The project uses a **`src/` layout** (`src/unbox/`).  
Extractor registration is fully automatic via `BaseExtractor.__init_subclass__`:

1. [src/unbox/base.py](../src/unbox/base.py) — `BaseExtractor` ABC and the `_registry` dict.
2. [src/unbox/extractors/](../src/unbox/extractors/) — one module per format (pdf.py, docx.py, pptx.py). Each subclasses `BaseExtractor`, sets `supported_extensions`, and implements `extract(file_path) -> str`.
3. [src/unbox/extractors/\_\_init\_\_.py](../src/unbox/extractors/__init__.py) — imports every extractor module to trigger registration. **New extractors must be imported here.**
4. [src/unbox/registry.py](../src/unbox/registry.py) — public lookup API: `get_extractor(ext)` / `list_supported_extensions()`.
5. [src/unbox/cli.py](../src/unbox/cli.py) — argparse CLI entry point (`main(argv=None) -> int`).

### Adding a new format

1. Create `src/unbox/extractors/<fmt>.py` — subclass `BaseExtractor`, set `supported_extensions`, implement `extract`.
2. Add the import to `src/unbox/extractors/__init__.py`.
3. Add the library to `dependencies` in `pyproject.toml`.

## Build and Test

```bash
pip install -e ".[dev]"        # install with dev deps (pytest, ruff)
ruff check src/ tests/         # lint
ruff format src/ tests/        # format
pytest tests/ -v               # run tests
unbox sample.pdf               # run CLI
```

## Project Conventions

- Entry point uses `main(argv: list[str] | None = None) -> int` pattern with `raise SystemExit(main())`.
- `# noqa:` comments are specific-code only (`F401` for side-effect imports, `BLE001` for intentional broad except in CLI).
- Tests use **class grouping** (`class TestPdfExtractor`), `unittest.mock.patch` to mock third-party I/O libraries, and `tmp_path`/`capsys` fixtures. See [tests/test_pdf.py](../tests/test_pdf.py).
- Hatchling is the build backend; wheel config maps `src/unbox` via `[tool.hatch.build.targets.wheel]`.

"""Command-line interface for unbox."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from unbox import __version__
from unbox.registry import get_extractor, list_supported_extensions


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="unbox",
        description="Extract text content from PDF, PowerPoint, and Word files.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="One or more files to extract text from.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to write .txt output files (default: same directory as input).",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print extracted text to stdout instead of writing files.",
    )
    parser.add_argument(
        "--list-formats",
        action="store_true",
        help="List all supported file formats and exit.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def _resolve_output_path(input_path: Path, output_dir: Path | None) -> Path:
    """Determine the output ``.txt`` path for a given input file."""
    stem = input_path.stem
    target_dir = output_dir if output_dir is not None else input_path.parent
    return target_dir / f"{stem}.txt"


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``unbox`` CLI.

    Parameters
    ----------
    argv:
        Command-line arguments (defaults to ``sys.argv[1:]``).

    Returns
    -------
    int
        Exit code — 0 on success, 1 on error.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    # Handle --list-formats
    if args.list_formats:
        extensions = list_supported_extensions()
        print("Supported formats:")
        for ext in extensions:
            print(f"  {ext}")
        return 0

    # Require at least one file when not listing formats
    if not args.files:
        parser.error("the following arguments are required: files")

    # Create output directory if needed
    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)

    errors: list[str] = []

    for file_path in args.files:
        file_path = Path(file_path).resolve()

        # Validate input file
        if not file_path.exists():
            errors.append(f"File not found: {file_path}")
            continue
        if not file_path.is_file():
            errors.append(f"Not a file: {file_path}")
            continue

        extension = file_path.suffix.lower()

        # Get the extractor
        try:
            extractor = get_extractor(extension)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        # Extract text
        try:
            text = extractor.extract(file_path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Error extracting '{file_path.name}': {exc}")
            continue

        # Output
        if args.stdout:
            print(f"=== {file_path.name} ===")
            print(text)
            print()
        else:
            out_path = _resolve_output_path(file_path, args.output_dir)
            out_path.write_text(text, encoding="utf-8")
            print(f"Extracted: {file_path.name} -> {out_path}")

    # Report errors
    if errors:
        print("\nErrors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

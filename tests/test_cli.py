"""Tests for the CLI module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from unbox.cli import main


class TestCliListFormats:
    """Tests for --list-formats flag."""

    def test_list_formats_exits_zero(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Verify --list-formats prints all formats and exits with code 0."""
        result = main(["--list-formats"])
        assert result == 0
        captured = capsys.readouterr()
        assert ".pdf" in captured.out
        assert ".pptx" in captured.out
        assert ".docx" in captured.out


class TestCliVersion:
    """Tests for --version flag."""

    def test_version_flag(self) -> None:
        """Verify --version raises SystemExit with code 0."""
        with pytest.raises(SystemExit, match="0"):
            main(["--version"])


class TestCliFileValidation:
    """Tests for input file validation."""

    def test_missing_file_returns_error(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Verify a missing file produces an error message and exit code 1."""
        result = main(["nonexistent_file.pdf"])
        assert result == 1
        captured = capsys.readouterr()
        assert "File not found" in captured.err

    def test_unsupported_format_returns_error(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Verify an unsupported extension produces an error and exit code 1."""
        fake_file = tmp_path / "test.xyz"
        fake_file.write_text("content")
        result = main([str(fake_file)])
        assert result == 1
        captured = capsys.readouterr()
        assert "Unsupported file format" in captured.err


class TestCliExtraction:
    """Tests for end-to-end extraction via CLI."""

    @patch("unbox.cli.get_extractor")
    def test_extract_to_file(
        self,
        mock_get: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Verify extraction writes correct content to a .txt file."""
        input_file = tmp_path / "sample.pdf"
        input_file.write_text("dummy")

        mock_extractor = mock_get.return_value
        mock_extractor.extract.return_value = "Extracted text content"

        result = main([str(input_file), "--output-dir", str(tmp_path)])

        assert result == 0
        output_file = tmp_path / "sample.txt"
        assert output_file.exists()
        assert output_file.read_text(encoding="utf-8") == "Extracted text content"

    @patch("unbox.cli.get_extractor")
    def test_extract_to_stdout(
        self,
        mock_get: MagicMock,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Verify --stdout prints extracted text to the console."""
        input_file = tmp_path / "sample.pdf"
        input_file.write_text("dummy")

        mock_extractor = mock_get.return_value
        mock_extractor.extract.return_value = "Stdout output"

        result = main([str(input_file), "--stdout"])

        assert result == 0
        captured = capsys.readouterr()
        assert "Stdout output" in captured.out

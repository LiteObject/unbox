"""Tests for the Word extractor."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from unbox.extractors.docx import DocxExtractor


class TestDocxExtractor:
    """Tests for DocxExtractor."""

    def test_supported_extensions(self) -> None:
        assert DocxExtractor.supported_extensions == [".docx"]

    @patch("unbox.extractors.docx.Document")
    def test_extract_paragraphs(self, mock_doc_cls: MagicMock) -> None:
        para1 = MagicMock()
        para1.text = "First paragraph"
        para2 = MagicMock()
        para2.text = "Second paragraph"

        mock_doc = MagicMock()
        mock_doc.paragraphs = [para1, para2]
        mock_doc.tables = []
        mock_doc_cls.return_value = mock_doc

        extractor = DocxExtractor()
        result = extractor.extract(Path("test.docx"))

        assert "First paragraph" in result
        assert "Second paragraph" in result

    @patch("unbox.extractors.docx.Document")
    def test_extract_tables(self, mock_doc_cls: MagicMock) -> None:
        cell1 = MagicMock()
        cell1.text = "A"
        cell2 = MagicMock()
        cell2.text = "B"
        row = MagicMock()
        row.cells = [cell1, cell2]
        table = MagicMock()
        table.rows = [row]

        mock_doc = MagicMock()
        mock_doc.paragraphs = []
        mock_doc.tables = [table]
        mock_doc_cls.return_value = mock_doc

        extractor = DocxExtractor()
        result = extractor.extract(Path("test.docx"))

        assert "A | B" in result

    @patch("unbox.extractors.docx.Document")
    def test_extract_skips_empty_paragraphs(self, mock_doc_cls: MagicMock) -> None:
        para = MagicMock()
        para.text = "   "

        mock_doc = MagicMock()
        mock_doc.paragraphs = [para]
        mock_doc.tables = []
        mock_doc_cls.return_value = mock_doc

        extractor = DocxExtractor()
        result = extractor.extract(Path("test.docx"))

        assert result == ""

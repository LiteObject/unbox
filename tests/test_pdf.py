"""Tests for the PDF extractor."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from unbox.extractors.pdf import PdfExtractor


class TestPdfExtractor:
    """Tests for PdfExtractor."""

    def test_supported_extensions(self) -> None:
        assert PdfExtractor.supported_extensions == [".pdf"]

    @patch("unbox.extractors.pdf.fitz")
    def test_extract_returns_text(self, mock_fitz: MagicMock) -> None:
        # Set up mock pages
        page1 = MagicMock()
        page1.get_text.return_value = "Page 1 content"
        page2 = MagicMock()
        page2.get_text.return_value = "Page 2 content"

        mock_doc = MagicMock()
        mock_doc.__enter__ = MagicMock(return_value=mock_doc)
        mock_doc.__exit__ = MagicMock(return_value=False)
        mock_doc.__iter__ = MagicMock(return_value=iter([page1, page2]))
        mock_fitz.open.return_value = mock_doc

        extractor = PdfExtractor()
        result = extractor.extract(Path("test.pdf"))

        assert "Page 1 content" in result
        assert "Page 2 content" in result

    @patch("unbox.extractors.pdf.fitz")
    def test_extract_skips_blank_pages(self, mock_fitz: MagicMock) -> None:
        page1 = MagicMock()
        page1.get_text.return_value = "Content"
        page2 = MagicMock()
        page2.get_text.return_value = "   \n  "  # blank

        mock_doc = MagicMock()
        mock_doc.__enter__ = MagicMock(return_value=mock_doc)
        mock_doc.__exit__ = MagicMock(return_value=False)
        mock_doc.__iter__ = MagicMock(return_value=iter([page1, page2]))
        mock_fitz.open.return_value = mock_doc

        extractor = PdfExtractor()
        result = extractor.extract(Path("test.pdf"))

        assert result == "Content"

    def test_repr(self) -> None:
        extractor = PdfExtractor()
        assert "PdfExtractor" in repr(extractor)

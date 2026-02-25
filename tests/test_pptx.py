"""Tests for the PowerPoint extractor."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from unbox.extractors.pptx import PptxExtractor


class TestPptxExtractor:
    """Tests for PptxExtractor."""

    def test_supported_extensions(self) -> None:
        assert PptxExtractor.supported_extensions == [".pptx"]

    @patch("unbox.extractors.pptx.Presentation")
    def test_extract_returns_text(self, mock_prs_cls: MagicMock) -> None:
        # Build mock slide with text
        paragraph = MagicMock()
        paragraph.text = "Hello World"
        text_frame = MagicMock()
        text_frame.paragraphs = [paragraph]
        shape = MagicMock()
        shape.has_text_frame = True
        shape.text_frame = text_frame
        slide = MagicMock()
        slide.shapes = [shape]

        mock_prs = MagicMock()
        mock_prs.slides = [slide]
        mock_prs_cls.return_value = mock_prs

        extractor = PptxExtractor()
        result = extractor.extract(Path("test.pptx"))

        assert "Hello World" in result
        assert "Slide 1" in result

    @patch("unbox.extractors.pptx.Presentation")
    def test_extract_skips_shapes_without_text(self, mock_prs_cls: MagicMock) -> None:
        shape = MagicMock()
        shape.has_text_frame = False
        slide = MagicMock()
        slide.shapes = [shape]

        mock_prs = MagicMock()
        mock_prs.slides = [slide]
        mock_prs_cls.return_value = mock_prs

        extractor = PptxExtractor()
        result = extractor.extract(Path("test.pptx"))

        # Only the slide header, no content → empty result
        assert result == ""

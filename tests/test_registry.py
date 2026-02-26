"""Tests for the extractor registry."""

from __future__ import annotations

import pytest

from unbox.registry import get_extractor, list_supported_extensions


class TestListSupportedExtensions:
    """Tests for list_supported_extensions."""

    def test_returns_all_three_formats(self) -> None:
        """Verify all three format extensions are registered."""
        extensions = list_supported_extensions()
        assert ".pdf" in extensions
        assert ".pptx" in extensions
        assert ".docx" in extensions

    def test_returns_sorted(self) -> None:
        """Verify extensions are returned in sorted order."""
        extensions = list_supported_extensions()
        assert extensions == sorted(extensions)


class TestGetExtractor:
    """Tests for get_extractor."""

    @pytest.mark.parametrize("ext", [".pdf", ".pptx", ".docx"])
    def test_returns_extractor_for_supported_extension(self, ext: str) -> None:
        """Verify each supported extension returns a valid extractor."""
        extractor = get_extractor(ext)
        assert extractor is not None
        assert ext in extractor.supported_extensions

    def test_case_insensitive_lookup(self) -> None:
        """Verify extension lookup is case-insensitive."""
        extractor = get_extractor(".PDF")
        assert ".pdf" in extractor.supported_extensions

    def test_raises_for_unsupported_extension(self) -> None:
        """Verify ValueError is raised for an unknown extension."""
        with pytest.raises(ValueError, match="Unsupported file format"):
            get_extractor(".xyz")

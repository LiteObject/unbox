"""Extractor registry — look up extractors by file extension."""

from __future__ import annotations

# Ensure all extractor modules are imported so they auto-register.
import unbox.extractors  # noqa: F401
from unbox.base import BaseExtractor, _registry


def get_extractor(extension: str) -> BaseExtractor:
    """Return an extractor instance for the given file *extension*.

    Parameters
    ----------
    extension:
        A file extension including the leading dot (e.g. ``".pdf"``).

    Raises
    ------
    ValueError
        If no extractor is registered for the extension.
    """
    normalized = (
        extension.lower() if extension.startswith(".") else f".{extension.lower()}"
    )
    cls = _registry.get(normalized)
    if cls is None:
        supported = ", ".join(sorted(_registry.keys()))
        msg = f"Unsupported file format: '{extension}'. Supported formats: {supported}"
        raise ValueError(msg)
    return cls()


def list_supported_extensions() -> list[str]:
    """Return a sorted list of all registered file extensions."""
    return sorted(_registry.keys())

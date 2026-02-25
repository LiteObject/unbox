"""PDF text extractor using PyMuPDF."""

from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF

from unbox.base import BaseExtractor


class PdfExtractor(BaseExtractor):
    """Extract plain text from PDF files."""

    supported_extensions = [".pdf"]

    def extract(self, file_path: Path) -> str:
        """Extract text from all pages of a PDF document.

        Parameters
        ----------
        file_path:
            Path to the ``.pdf`` file.

        Returns
        -------
        str
            Concatenated text from every page, separated by newlines.
        """
        pages: list[str] = []
        with fitz.open(file_path) as doc:
            for page in doc:
                text = page.get_text()
                if text.strip():
                    pages.append(text.strip())
        return "\n\n".join(pages)

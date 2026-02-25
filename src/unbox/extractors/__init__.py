"""Auto-import all extractor modules so they register via __init_subclass__."""

from unbox.extractors.docx import DocxExtractor
from unbox.extractors.pdf import PdfExtractor
from unbox.extractors.pptx import PptxExtractor

__all__ = ["DocxExtractor", "PdfExtractor", "PptxExtractor"]

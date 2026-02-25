"""Base extractor interface with auto-registration."""

from __future__ import annotations

import abc
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    pass

# Global registry: file extension -> extractor class.
# Typed loosely here to avoid forward-reference issues; the actual values
# are always ``type[BaseExtractor]`` subclasses.
_registry: dict[str, type] = {}


class BaseExtractor(abc.ABC):
    """Abstract base class for all format extractors.

    Subclasses are automatically registered by extension when they are defined,
    thanks to ``__init_subclass__``.  To create a new extractor:

    1. Create a new module under ``unbox/extractors/``.
    2. Subclass ``BaseExtractor``.
    3. Set the ``supported_extensions`` class variable (e.g. ``[".pdf"]``).
    4. Implement the ``extract`` method.
    5. Import the new module in ``unbox/extractors/__init__.py``.
    """

    supported_extensions: ClassVar[list[str]]
    """File extensions this extractor handles (e.g. ``[".pdf"]``)."""

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Register concrete subclasses by their supported extensions."""
        super().__init_subclass__(**kwargs)
        # Skip registration for abstract intermediaries
        if abc.ABC in cls.__bases__:
            return
        for ext in cls.supported_extensions:
            normalized = ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            _registry[normalized] = cls

    @abc.abstractmethod
    def extract(self, file_path: Path) -> str:
        """Extract text content from *file_path* and return it as a string.

        Parameters
        ----------
        file_path:
            Path to the source document.

        Returns
        -------
        str
            The extracted plain-text content.
        """

    def __repr__(self) -> str:
        return f"<{type(self).__name__} extensions={self.supported_extensions}>"

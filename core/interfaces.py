from typing import List, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


@runtime_checkable
class IDocumentParser(Protocol):
    """Abstract interface for extracting text content from document files."""

    def extract_text(self, file_path: str) -> str:
        """Extracts and returns plain text from a given file path.

        Args:
            file_path (str): Path to the source document file.

        Returns:
            str: Raw or parsed text extracted from the file.
        """
        ...


@runtime_checkable
class IRepository(Protocol[T]):
    """Generic repository protocol for domain record persistence and retrieval."""

    def save(self, record: T, destination: str) -> None:
        """Persists a record to the target destination.

        Args:
            record (T): The domain object or data dictionary to persist.
            destination (str): File path, URI, or connection string for storage.
        """
        ...

    def load(self, destination: str) -> List[T]:
        """Loads and returns stored records from the target destination.

        Args:
            destination (str): Storage location to retrieve records from.

        Returns:
            List[T]: List of retrieved records.
        """
        ...
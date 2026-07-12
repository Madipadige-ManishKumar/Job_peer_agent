import logging
from pathlib import Path
from pypdf import PdfReader

from core.interfaces import IDocumentParser

logger = logging.getLogger("AIRecruitmentPipeline")


class PdfDocumentParser(IDocumentParser):
    """Concrete implementation of IDocumentParser using PyPDF."""

    def extract_text(self, file_path: str) -> str:
        """Extracts text content from a target PDF file."""
        path = Path(file_path)
        if not path.exists():
            logger.error(f"PDF file not found at path: '{file_path}'")
            return f"Error: PDF file not found at path '{file_path}'"

        try:
            reader = PdfReader(str(path))
            pages_text = []
            for index, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted:
                    pages_text.append(extracted.strip())
                else:
                    logger.warning(f"No text on page {index + 1} of '{file_path}'")

            text = "\n".join(pages_text).strip()
            if not text:
                logger.warning(f"Extracted empty text from PDF: '{file_path}'")
                return "Empty PDF content."

            logger.info(f"Extracted {len(text)} chars from PDF: '{file_path}'")
            return text

        except Exception as e:
            logger.error(f"Failed to extract text from PDF '{file_path}': {e}", exc_info=True)
            return f"Error reading PDF: {e}"


class TextDocumentParser(IDocumentParser):
    """Concrete implementation of IDocumentParser for raw text files."""

    def extract_text(self, file_path: str) -> str:
        """Reads text from a plain text file."""
        path = Path(file_path)
        if not path.exists():
            logger.error(f"Text file not found at path: '{file_path}'")
            return f"Error: Text file not found at path '{file_path}'"

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if not content:
                logger.warning(f"Text file is empty: '{file_path}'")
                return "Empty document content."

            logger.info(f"Read {len(content)} chars from file: '{file_path}'")
            return content

        except Exception as e:
            logger.error(f"Failed to read file '{file_path}': {e}", exc_info=True)
            return f"Error reading file: {e}"
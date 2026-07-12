import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from core.interfaces import IRepository

logger = logging.getLogger("AIRecruitmentPipeline")


class JsonCandidateRepository(IRepository[Dict[str, Any]]):
    """Concrete repository for persisting candidate records into local JSON files."""

    def save(self, record: Dict[str, Any], destination: str) -> None:
        """Appends candidate evaluation record to JSON file."""
        dest_path = Path(destination)

        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            data = self.load(destination)
            data.append(record)

            with open(dest_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(
                f"Persisted record for '{record.get('candidate_name', 'Unknown')}' to '{destination}'"
            )

        except Exception as e:
            logger.error(f"Failed to persist record to '{destination}': {e}", exc_info=True)

    def load(self, destination: str) -> List[Dict[str, Any]]:
        """Reads candidate records from JSON file."""
        dest_path = Path(destination)
        if not dest_path.exists():
            logger.info(f"Storage file '{destination}' does not exist yet.")
            return []

        try:
            with open(dest_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)

        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Could not parse JSON at '{destination}': {e}.")
            return []
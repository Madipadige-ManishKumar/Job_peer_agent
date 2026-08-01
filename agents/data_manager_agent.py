import logging
from typing import Any, Dict
from autogen_core import (
    MessageContext,
    RoutedAgent,
    TopicId,
    message_handler,
    type_subscription,
)

from core.interfaces import IRepository
from core.messages import PipelineCompletedEvent, SaveCandidateRecordCommand

logger = logging.getLogger("AIRecruitmentPipeline")

SCREENING_TOPIC = TopicId(type="screening_workflow", source="default")

@type_subscription(topic_type="screening_workflow")
class DataManagerAgent(RoutedAgent):
    """Manages record persistence via repository abstraction and broadcasts workflow completion."""

    def __init__(self, repository: IRepository[Dict[str, Any]]) -> None:
        super().__init__("DataManagerAgent")
        self._repository = repository

    @message_handler
    async def handle_save_command(
        self, message: SaveCandidateRecordCommand, ctx: MessageContext
    ) -> None:
        logger.info(
            f"[{self.id.type}] Direct command received. Persisting candidate '{message.candidate_name}'"
        )

        record = {
            "candidate_name": message.candidate_name,
            "match_score": message.match_score,
            "summary": message.summary,
        }

        self._repository.save(record, message.output_path)

        logger.info(f"[{self.id.type}] Record saved. Broadcasting PipelineCompletedEvent.")

        await self.publish_message(
            PipelineCompletedEvent(
                candidate_name=message.candidate_name,
                status="SUCCESS",
                record_file=message.output_path,
            ),
            topic_id=SCREENING_TOPIC,
        )
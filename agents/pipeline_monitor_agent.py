import asyncio
import logging
from autogen_core import (
    MessageContext,
    RoutedAgent,
    default_subscription,
    message_handler,
    type_subscription,
)

from core.messages import PipelineCompletedEvent

logger = logging.getLogger("AIRecruitmentPipeline")


@type_subscription(topic_type="screening_workflow")
class PipelineMonitorAgent(RoutedAgent):
    """Monitors completion events broadcast across the screening workflow topic."""

    def __init__(self, completion_future: asyncio.Future) -> None:
        super().__init__("PipelineMonitorAgent")
        self._completion_future = completion_future

    @message_handler
    async def handle_completion(
        self, message: PipelineCompletedEvent, ctx: MessageContext
    ) -> None:
        logger.info(
            f"[{self.id.type}] Workflow completed for candidate '{message.candidate_name}'. "
            f"Status: {message.status} | Storage: '{message.record_file}'"
        )
        if not self._completion_future.done():
            self._completion_future.set_result(True)
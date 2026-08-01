import logging
from autogen_core import (
    MessageContext,
    RoutedAgent,
    TopicId,
    default_subscription,
    message_handler,
    type_subscription,
)
from core.interfaces import IDocumentParser
from core.messages import ResumeParsedEvent, StartScreeningCommand

logger = logging.getLogger("AIRecruitmentPipeline")

SCREENING_TOPIC = TopicId(type="screening_workflow", source="default")


@type_subscription(topic_type="screening_workflow")
class ResumeParserAgent(RoutedAgent):
    """Parses PDF resumes and job description files, broadcasting structured text events."""

    def __init__(
        self,
        pdf_parser: IDocumentParser,
        text_parser: IDocumentParser,
    ) -> None:
        super().__init__("ResumeParserAgent")
        self._pdf_parser = pdf_parser
        self._text_parser = text_parser

    @message_handler
    async def handle_start_command(
        self, message: StartScreeningCommand, ctx: MessageContext
    ) -> None:
        logger.info(
            f"[{self.id.type}] Processing resume '{message.resume_pdf_path}' and JD '{message.job_desc_path}'"
        )

        resume_text = self._pdf_parser.extract_text(message.resume_pdf_path)
        jd_text = self._text_parser.extract_text(message.job_desc_path)

        logger.info(f"[{self.id.type}] Text extraction complete. Publishing ResumeParsedEvent to broadcast topic.")

        await self.publish_message(
            ResumeParsedEvent(
                candidate_name=message.candidate_name,
                resume_text=resume_text,
                job_description_text=jd_text,
                required_skills=message.required_skills,
            ),
            topic_id=SCREENING_TOPIC,
        )
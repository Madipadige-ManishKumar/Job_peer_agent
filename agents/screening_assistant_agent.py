import json
import logging
from typing import List, Tuple
from autogen_core import (
    AgentId,
    MessageContext,
    RoutedAgent,
    default_subscription,
    message_handler,
    type_subscription,
)
from autogen_core.models import SystemMessage, UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from core.messages import ResumeParsedEvent, SaveCandidateRecordCommand

logger = logging.getLogger("AIRecruitmentPipeline")


@type_subscription(topic_type="screening_workflow")
class ScreeningAssistantAgent(RoutedAgent):
    """Evaluates candidate qualifications against JD requirements using local LLM context."""

    def __init__(self, model_client: OpenAIChatCompletionClient) -> None:
        super().__init__("ScreeningAssistantAgent")
        self._model_client = model_client
        self._system_prompt = (
            "You are an expert HR Screening Assistant. Evaluate candidate suitability "
            "based on required skills and output a JSON evaluation matching the exact keys: "
            '{"match_score": <float 0-100>, "summary": "<concise fit summary>"}.'
        )

    @message_handler
    async def handle_parsed_resume(
        self, message: ResumeParsedEvent, ctx: MessageContext
    ) -> None:
        logger.info(f"[{self.id.type}] Evaluating candidate fit for: '{message.candidate_name}'")

        match_stats = self._perform_keyword_match(
            message.required_skills, message.resume_text
        )

        messages_context = [
            SystemMessage(content=self._system_prompt),
            UserMessage(
                content=f"""
Candidate Name: {message.candidate_name}
Required Skills: {message.required_skills}
Keyword Match Stats: {match_stats}

Job Description:
{message.job_description_text[:1000]}

Candidate Resume Text:
{message.resume_text[:2000]}
""",
                source="user",
            ),
        ]

        response = await self._model_client.create(messages=messages_context)
        llm_output = str(response.content)

        logger.info(f"[{self.id.type}] LLM analysis completed successfully.")

        score, summary = self._parse_llm_response(
            llm_output, fallback_score=match_stats["match_score"]
        )

        data_manager_id = AgentId("DataManagerAgent", "default")
        logger.info(
            f"[{self.id.type}] Sending direct SaveCandidateRecordCommand to {data_manager_id}"
        )

        await self.send_message(
            SaveCandidateRecordCommand(
                candidate_name=message.candidate_name,
                match_score=score,
                summary=summary,
            ),
            recipient=data_manager_id,
        )

    def _perform_keyword_match(self, required_skills: List[str], text: str) -> dict:
        text_lower = text.lower()
        matched = [s for s in required_skills if s.lower() in text_lower]
        total = len(required_skills)
        score = round((len(matched) / total) * 100, 2) if total > 0 else 0.0
        return {"matched": matched, "match_score": score}

    def _parse_llm_response(
        self, content: str, fallback_score: float
    ) -> Tuple[float, str]:
        try:
            clean_content = content.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_content)
            return float(data.get("match_score", fallback_score)), str(
                data.get("summary", content)
            )
        except Exception:
            return fallback_score, content.strip()
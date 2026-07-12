import logging
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient

from config.model_config import ModelConfig

logger = logging.getLogger("AIRecruitmentPipeline")


def get_model_client(cfg: ModelConfig = ModelConfig()) -> OpenAIChatCompletionClient:
    """Factory function producing completion client configured for local llama-server."""
    logger.info(f"Initializing OpenAIChatCompletionClient connected to: {cfg.base_url}")

    return OpenAIChatCompletionClient(
        model=cfg.model,
        base_url=cfg.base_url,
        api_key=cfg.api_key,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.UNKNOWN,
        },
        temperature=cfg.temperature,
    )
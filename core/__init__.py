"""Core abstractions, protocols, and message contracts for the AI Recruitment Agent."""

from .interfaces import IDocumentParser, IRepository
from .messages import (
    PipelineCompletedEvent,
    ResumeParsedEvent,
    SaveCandidateRecordCommand,
    StartScreeningCommand,
)

__all__ = [
    "IDocumentParser",
    "IRepository",
    "StartScreeningCommand",
    "ResumeParsedEvent",
    "SaveCandidateRecordCommand",
    "PipelineCompletedEvent",
]
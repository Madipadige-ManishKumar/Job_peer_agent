from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class StartScreeningCommand:
    """Command payload issued to initiate the candidate evaluation process."""

    candidate_name: str
    resume_pdf_path: str
    job_desc_path: str
    required_skills: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ResumeParsedEvent:
    """Event payload published after raw candidate resume and job description text are extracted."""

    candidate_name: str
    resume_text: str
    job_description_text: str
    required_skills: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class SaveCandidateRecordCommand:
    """Direct message command sent to the persistence manager containing screening results."""

    candidate_name: str
    match_score: float
    summary: str
    output_path: str = "candidate_records.json"


@dataclass(frozen=True)
class PipelineCompletedEvent:
    """Event payload broadcast upon successful candidate record persistence."""

    candidate_name: str
    status: str
    record_file: str
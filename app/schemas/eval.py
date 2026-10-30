from enum import Enum

from pydantic import BaseModel


class EvalCase(BaseModel):
    id: str
    input: str
    expected_concept: str


class InferenceResult(EvalCase):
    model: str
    raw_output: str


class JudgeType(str, Enum):
    deterministic = "deterministic"
    llm = "llm"


class JudgeScore(BaseModel):
    passed: bool
    reason: str


class ScoredResult(InferenceResult):
    passed: bool
    judge: JudgeType
    reason: str | None = None


class InferenceRequest(BaseModel):
    model: str | None = None
    case_ids: list[str] | None = None


class ScoringRequest(BaseModel):
    results: list[InferenceResult]
    judge: JudgeType = JudgeType.deterministic
    judge_model: str | None = None


class LogSummary(BaseModel):
    total: int
    passed: int
    pass_rate: float

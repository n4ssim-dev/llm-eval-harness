import asyncio

import litellm

from app.core.config import get_settings
from app.schemas.eval import InferenceResult, JudgeScore, JudgeType, ScoredResult


def deterministic_judge(result: InferenceResult) -> ScoredResult:
    passed = result.expected_concept.lower() in result.raw_output.lower()
    return ScoredResult(**result.model_dump(), passed=passed, judge=JudgeType.deterministic)


async def llm_judge(result: InferenceResult, judge_model: str) -> ScoredResult:
    settings = get_settings()
    prompt = (
        f"Input: {result.input}\n"
        f"Response: {result.raw_output}\n"
        f"Criteria: {result.expected_concept}\n"
        "Did the response meet the criteria? Reply as JSON."
    )
    response = await litellm.acompletion(
        model=judge_model,
        messages=[{"role": "user", "content": prompt}],
        response_format=JudgeScore,
        api_key=settings.llm_api_key,
        num_retries=settings.llm_num_retries,
        timeout=settings.llm_timeout,
    )
    score = JudgeScore.model_validate_json(response.choices[0].message.content)
    return ScoredResult(
        **result.model_dump(), passed=score.passed, reason=score.reason, judge=JudgeType.llm
    )


async def score_results(
    results: list[InferenceResult], judge: JudgeType, judge_model: str | None = None
) -> list[ScoredResult]:
    if judge is JudgeType.deterministic:
        return [deterministic_judge(r) for r in results]
    model = judge_model or get_settings().default_judge_model
    return await asyncio.gather(*(llm_judge(r, model) for r in results))

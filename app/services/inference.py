import asyncio

import litellm

from app.core.config import get_settings
from app.schemas.eval import EvalCase, InferenceResult


async def run_case(case: EvalCase, model: str) -> InferenceResult:
    settings = get_settings()
    response = await litellm.acompletion(
        model=model,
        messages=[{"role": "user", "content": case.input}],
        api_key=settings.llm_api_key,
        num_retries=settings.llm_num_retries,
        timeout=settings.llm_timeout,
    )
    raw = response.choices[0].message.content or ""
    return InferenceResult(**case.model_dump(), model=model, raw_output=raw)


async def run_cases(cases: list[EvalCase], model: str) -> list[InferenceResult]:
    return await asyncio.gather(*(run_case(case, model) for case in cases))

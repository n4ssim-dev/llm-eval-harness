import asyncio
import litellm
from fastapi import FastAPI
from .routes.logging import router as logging_router
from .routes.scoring import router as scoring_router
from .routes.inference import router as inference_router

app = FastAPI()
app.include_router(logging_router)
app.include_router(scoring_router)
app.include_router(inference_router)


async def run_case(case: dict, model: str ) -> dict:
    response = await litellm.acompletion(
        model=model,
        messages=[{"role": "user", "content": case["input"]}],
        num_retries=3,
        timeout=30,
    )
    raw = response.choices[0].message.content
    return {**case, "raw_input": raw}

def deterministic_judge(result: dict) -> dict:
    output = result["raw_output"].lower()
    concept = result["expected_concept"].lower()
    passed = concept in output
    return {**result, "passed": passed, "judge": "deterministic"}
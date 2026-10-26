import asyncio
import litellm

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
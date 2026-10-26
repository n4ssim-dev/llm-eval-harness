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


from pydantic import BaseModel
import litellm

class JudgeScore(BaseModel):
    passed: bool
    reason: str

async def llm_judge(result: dict, judge_model: str) -> dict:
    prompt = f"Input: {result['input']}\nResponse: {result['raw_output']}\nCriteria: {result['expected_concept']}\nDid the response meet the criteria? Reply as JSON."
    response = await litellm.acompletion(
        model=judge_model,
        messages=[{"role": "user", "content": prompt}],
        response_format=JudgeScore,
    )
    score = JudgeScore.model_validate_json(response.choices[0].message.content)
    return {**result, "passed": score.passed, "reason": score.reason, "judge": "llm"}
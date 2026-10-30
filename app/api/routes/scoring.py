from fastapi import APIRouter

from app.schemas.eval import ScoredResult, ScoringRequest
from app.services.logger import write_results
from app.services.scoring import score_results

router = APIRouter(prefix="/scoring", tags=["scoring"])


@router.post("/", response_model=list[ScoredResult])
async def score(request: ScoringRequest):
    scored = await score_results(request.results, request.judge, request.judge_model)
    write_results(scored)
    return scored

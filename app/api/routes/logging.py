from fastapi import APIRouter

from app.schemas.eval import LogSummary, ScoredResult
from app.services.logger import read_results, summarize

router = APIRouter(prefix="/logging", tags=["logging"])


@router.get("/results", response_model=list[ScoredResult])
def get_results():
    return read_results()


@router.get("/summary", response_model=LogSummary)
def get_summary():
    return summarize(read_results())

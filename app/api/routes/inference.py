from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.schemas.eval import EvalCase, InferenceRequest, InferenceResult
from app.services.dataset import load_dataset
from app.services.inference import run_cases

router = APIRouter(prefix="/inference", tags=["inference"])


@router.get("/dataset", response_model=list[EvalCase])
def get_dataset():
    return load_dataset()


@router.post("/run", response_model=list[InferenceResult])
async def run_inference(request: InferenceRequest):
    cases = load_dataset(request.case_ids)
    if not cases:
        raise HTTPException(status_code=404, detail="No matching cases in dataset")
    return await run_cases(cases, request.model or get_settings().default_model)

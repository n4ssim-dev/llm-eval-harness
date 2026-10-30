import json
from functools import lru_cache
from pathlib import Path

from app.core.config import get_settings
from app.schemas.eval import EvalCase


@lru_cache
def _load(path: Path) -> tuple[EvalCase, ...]:
    with path.open(encoding="utf-8") as f:
        return tuple(EvalCase.model_validate(case) for case in json.load(f))


def load_dataset(case_ids: list[str] | None = None) -> list[EvalCase]:
    cases = _load(get_settings().dataset_path)
    if case_ids is None:
        return list(cases)
    wanted = set(case_ids)
    return [case for case in cases if case.id in wanted]

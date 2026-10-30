from app.core.config import get_settings
from app.schemas.eval import LogSummary, ScoredResult


def write_results(results: list[ScoredResult]) -> None:
    path = get_settings().log_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for result in results:
            f.write(result.model_dump_json() + "\n")


def read_results() -> list[ScoredResult]:
    path = get_settings().log_path
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [ScoredResult.model_validate_json(line) for line in f if line.strip()]


def summarize(results: list[ScoredResult]) -> LogSummary:
    total = len(results)
    passed = sum(r.passed for r in results)
    return LogSummary(total=total, passed=passed, pass_rate=passed / total if total else 0.0)

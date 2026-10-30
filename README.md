# Custom LLM evaluation harness

Ce projet consiste à produire un harness d'évaluation pour des résultats LLM, structuré autour de 4 composants modulaire qui permettent un test et un scoring personnalisé des performances obtenu, à l'instar de Benchmark public plus généraliste (comme MMLMU ou GSM8K)

ces 4 composants modulaire nous permettant une bonne observability sont :
- un 'golden dataset' (on entend par là un jeu de données soigneusement sélectionnée, vérifiée et versionnée)
- un runner d'inférence (pour la couche llm)
- une couche de jugement
- un logger

Chaque couche se verra être volontairement minimale pour assurer l'adaption du projet à des exigeances/projets futur.

## Prérequis

`>=Python 3.10`

`Clé API LLM` 

## Structure

```
app/
├── main.py            # instance FastAPI + /health
├── core/config.py     # Settings (pydantic-settings, lit le .env)
├── schemas/eval.py    # modèles Pydantic (EvalCase, InferenceResult, ScoredResult…)
├── services/          # logique métier : dataset, inference, scoring, logger
└── api/
    ├── router.py      # agrège les routers
    └── routes/        # inference, scoring, logging
```

## Lancement

```bash
uv sync
uv run fastapi dev app/main.py
```

Documentation interactive : http://127.0.0.1:8000/docs

Variables `.env` : `LLM_API_KEY`, `DEFAULT_MODEL`, `DEFAULT_JUDGE_MODEL`, `LLM_TIMEOUT`, `LLM_NUM_RETRIES`, `DATASET_PATH`, `LOG_PATH`.

## Endpoints

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/inference/dataset` | liste le golden dataset |
| POST | `/inference/run` | exécute le modèle sur le dataset (`model`, `case_ids` optionnels) |
| POST | `/scoring/` | note des résultats (`judge`: `deterministic` ou `llm`) et les journalise |
| GET | `/logging/results` | résultats journalisés (`logs/results.jsonl`) |
| GET | `/logging/summary` | total / réussis / taux de réussite |

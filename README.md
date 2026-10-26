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
# Notes

## Time spent

Roughly 8–10 hours in total.

- Setup / Docker / PostgreSQL: ~2 hours
- Extract & load: ~1.5 hours
- dbt: ~1 hour
- Airflow: ~2 hours
- Notebook / validation / documentation: ~1.5–2 hours

## What I would do with more time

- Improve the Airflow backfill behavior and investigate the metadata deadlock encountered during a concurrent 30-day backfill.
- Add more robust retry and failure handling around API extraction and database operations.
- Add additional data-quality checks for temperature ranges and precipitation values.
- Add automated CI checks for the repository.

## Known gaps

- A concurrent 30-day Airflow backfill encountered an Airflow metadata database deadlock. Single logical-date DAG runs were validated successfully, and the complete 30-day raw dataset was validated using sequential ingestion.
- The pipeline currently uses a small configured set of cities rather than a larger dynamic city configuration.
- Airflow task-level retry configuration could be strengthened for production use.

## AI-usage declaration

I used ChatGPT for lookup, debugging, implementation review, and development assistance. I wrote, ran, tested, and reviewed the final implementation and can explain the code in an interview.

| Where (file / area) | What the tool did | What I changed afterwards |
| --- | --- | --- |
| `ingestion/weather_api.py` | Helped with Open-Meteo Python client usage and debugging API response handling. | Implemented and tested the extraction logic with the configured cities and verified the returned values. |
| `ingestion/load.py` | Helped review PostgreSQL connection and UPSERT/idempotency logic. | Implemented and tested the `(city, date)` conflict handling and verified reruns do not create duplicates. |
| `dags/weather_pipeline.py` | Helped with Airflow task dependencies, logical-date handling, and debugging PythonOperator/XCom behavior. | Implemented the DAG, tested logical-date execution, fixed the XCom data handling, and validated the complete task chain. |
| `dbt/` | Helped with dbt PostgreSQL configuration and test syntax, including the `data_tests` syntax used by the installed dbt version. | Implemented the staging model, mart, source configuration, documentation, and tests, then ran `dbt run` and `dbt test` successfully. |
| `notebooks/walkthrough.ipynb` | Helped structure the walkthrough notebook around extraction, loading, dbt execution, validation, and rerun safety. | Ran the notebook, verified the outputs, and reviewed the final notebook contents and results. |
| Documentation | Helped review README/notes structure and reproducibility requirements. | Updated the repository documentation and recorded the known limitations and AI usage. |
# Todo List API (FastAPI)

Esqueleto base del proyecto. El dominio real (usuarios y tareas, ver
`spec_estandares_modelo_datos.txt` y `spec_reglas_negocio_validaciones.txt`)
todavía no está implementado.

## Ejecutar

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

`GET /health` -> `{"status": "ok"}`

## Recurso de referencia: `sample_item`

Este repo incluye **un recurso de ejemplo ya implementado de punta a
punta** (`sample_item`) únicamente para mostrar el patrón arquitectónico
que el código nuevo debe replicar — no es parte del dominio Todo List y no
debe confundirse con `User`/`Task`:

- [`app/models/sample_item.py`](app/models/sample_item.py) — modelo SQLAlchemy.
- [`app/schemas/sample_item.py`](app/schemas/sample_item.py) — DTOs Pydantic.
- [`app/repositories/sample_item_repository.py`](app/repositories/sample_item_repository.py) — acceso a datos.
- [`app/services/sample_item_service.py`](app/services/sample_item_service.py) — lógica de negocio + excepción de dominio (`DuplicateSampleItemError`).
- [`app/api/routers/sample_item.py`](app/api/routers/sample_item.py) — router delgado con inyección de dependencias.
- [`app/main.py`](app/main.py) — registro del router y del exception handler central.
- [`tests/services/test_sample_item_service.py`](tests/services/test_sample_item_service.py) y [`tests/repositories/test_sample_item_repository.py`](tests/repositories/test_sample_item_repository.py) — pruebas en espejo (repositorio falso para el service, SQLite en memoria para el repository).

Endpoints: `POST /sample-items` (rechaza nombres duplicados con 409) y
`GET /sample-items`. Corre sobre SQLite en memoria por defecto (sin
depender de Postgres) solo para este ejemplo; el dominio real debe usar
`DATABASE_URL` (Postgres) tal como pide la especificación.

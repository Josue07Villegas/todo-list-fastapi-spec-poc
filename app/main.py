from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routers import sample_item
from app.core.database import Base, engine
from app.services.exceptions import DuplicateSampleItemError

app = FastAPI(title="Todo List API", version="0.1.0")

# Solo para el recurso de referencia sample_item (SQLite en memoria por
# defecto). El dominio real (User/Task) se debe crear via migraciones
# contra Postgres, no via create_all.
Base.metadata.create_all(bind=engine)

app.include_router(sample_item.router)


@app.exception_handler(DuplicateSampleItemError)
def handle_duplicate_sample_item(request: Request, exc: DuplicateSampleItemError) -> JSONResponse:
    # Exception handler central: traduce excepciones de dominio a la
    # respuesta HTTP correcta, para que routers/services no dependan de
    # FastAPI (ver spec_estandares_modelo_datos.txt seccion 3).
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

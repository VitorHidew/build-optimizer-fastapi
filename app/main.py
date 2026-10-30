from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.data import load_catalog
from app.engine import evaluate, optimize
from app.models import BuildRequest, BuildResult, Catalog


ROOT = Path(__file__).parents[1]
STATIC_DIR = ROOT / "static"

app = FastAPI(
    title="Otimizador de Builds Fictícias",
    description="API demonstrativa para comparar combinações de equipamentos inventados.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    load_catalog()
    return {"status": "ok", "dataset": "ficticio"}


@app.get("/api/catalog", response_model=Catalog)
def catalog() -> Catalog:
    return load_catalog()


@app.post("/api/evaluate", response_model=BuildResult)
def evaluate_build(request: BuildRequest) -> BuildResult:
    try:
        return evaluate(load_catalog(), request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/optimize", response_model=BuildResult)
def optimize_build(target_id: str = Query(min_length=1)) -> BuildResult:
    try:
        return optimize(load_catalog(), target_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

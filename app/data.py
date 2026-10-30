import json
from functools import lru_cache
from pathlib import Path

from app.models import Catalog


DATA_FILE = Path(__file__).parents[1] / "data" / "catalogo_ficticio.json"


@lru_cache(maxsize=1)
def load_catalog() -> Catalog:
    return Catalog.model_validate(json.loads(DATA_FILE.read_text(encoding="utf-8")))

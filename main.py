from fastapi import FastAPI
from sheep_compendium.models.db import db
from sheep_compendium.models.models import Sheep

app = FastAPI()


@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    return db.get_sheep(id)
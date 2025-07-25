from fastapi import FastAPI
from sheep_compendium.models.db import db #emily - had to change the code here if you have problems text me
from sheep_compendium.models.models import Sheep #emily - had to change the code here if you have problems text me

app = FastAPI()


@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    return db.get_sheep(id)
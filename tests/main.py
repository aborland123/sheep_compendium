from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep
from typing import List

app = FastAPI()


@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    return db.get_sheep(id)

@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    #Check if sheep ID already exists
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")
    #Add the new sheep to the database
    db.data[sheep.id] = sheep
    return sheep

# --- Extra Credit Endpoints ---
@app.delete("/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    if not db.delete_sheep(id):
        raise HTTPException(status_code=404, detail="Sheep not found")
    return

@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, sheep: Sheep):
    # Check if the IDs match
    if id != sheep.id:
        raise HTTPException(status_code=400, detail="Ids do not match")
    try:
        updated_sheep = db.update_sheep(id, sheep)
        return updated_sheep
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/sheep/", response_model=List[Sheep])
def read_all_sheep():
    return db.read_all_sheep()
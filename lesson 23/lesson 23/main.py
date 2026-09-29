from fastapi import FastAPI
from models import  Develeoper, Project

app = FastAPI()

@app.post("/developers/")
def create_developer(developer: Developer):
    return{"messaages":"Developer created successfully","developer":developer}


@app.post("/projets/")
def create_project(project:Project)
    return{"messagess":"Project created successfully","project":project}


from fastapi import FastAPI,HTTPExpection
from typing import List

import database
import models
from models import Movie,MovieCreate



app = FastAPI()

@app.get("/")
def read_root():
    return {"message":"Wellcome to the movies Crid API"}

@app.post("/movies/",response_model=Movie)
def create_movie(movie: MovieCreate):
    movie_id = database.create_movie(movie)
    return models.Movie(id=movie_id, **movie.diet())



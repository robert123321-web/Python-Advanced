from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class Category(CategoryCreate):
    id: int


class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    ingredients: str = Field(..., min_length=1)
    instructions: str = Field(..., min_length=1)
    category_id: int


class Recipe(RecipeCreate):
    id: int

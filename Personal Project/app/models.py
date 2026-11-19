
from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    category: str
    unit: str


class StoreCreate(BaseModel):
    name: str
    location: str = ""


class PriceCreate(BaseModel):
    product_id: int
    store_id: int
    price: float = Field(gt=0)


class ShoppingItemCreate(BaseModel):
    product_id: int
    quantity: float = Field(gt=0)


class BudgetCreate(BaseModel):
    amount: float = Field(gt=0)
    month: str


class ExpenseCreate(BaseModel):
    description: str
    amount: float = Field(gt=0)


class RecipeCreate(BaseModel):
    name: str
    instructions: str = ""
    preparation_time: int = Field(ge=0)


class PantryCreate(BaseModel):
    product_id: int
    quantity: float = Field(gt=0)
    expiry_date: Optional[str] = None


class MealPlanCreate(BaseModel):
    recipe_id: int
    plan_date: str
    meal_type: str


class OfferCreate(BaseModel):
    product_id: int
    store_id: int
    discount_price: float = Field(gt=0)
    expiry_date: Optional[str] = None

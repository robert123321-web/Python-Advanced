
from fastapi import FastAPI, HTTPException
from datetime import date
import sqlite3

import app.database as database
from app.models import (
    ProductCreate,
    StoreCreate,
    PriceCreate,
    ShoppingItemCreate,
    BudgetCreate,
    ExpenseCreate,
    RecipeCreate,
    PantryCreate,
    MealPlanCreate,
    OfferCreate
)

app = FastAPI(
    title="SmartBasket API",
    description="Intelligent Grocery Shopping and Meal Planning System",
    version="1.0.0"
)

database.initialize_database()


# HOME

@app.get("/")
def home():
    return {
        "message": "Welcome to SmartBasket!",
        "status": "Running",
        "documentation": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# PRODUCTS

@app.post("/products")
def create_product(product: ProductCreate):
    try:
        product_id = database.execute(
            """INSERT INTO products(name, category, unit)
               VALUES (?, ?, ?)""",
            (product.name, product.category, product.unit)
        )
        return {"message": "Product created", "id": product_id}
    except sqlite3.IntegrityError:
        raise HTTPException(400, "Product already exists")


@app.get("/products")
def get_products():
    return database.fetch_all("SELECT * FROM products ORDER BY name")


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = database.fetch_one(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    )
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        with database.connect() as db:
            cursor = db.execute(
                "DELETE FROM products WHERE id = ?", (product_id,)
            )
            if cursor.rowcount == 0:
                raise HTTPException(404, "Product not found")
        return {"message": "Product deleted"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            400, "Product is being used by another record"
        )


# STORES

@app.post("/stores")
def create_store(store: StoreCreate):
    store_id = database.execute(
        "INSERT INTO stores(name, location) VALUES (?, ?)",
        (store.name, store.location)
    )
    return {"message": "Store created", "id": store_id}


@app.get("/stores")
def get_stores():
    return database.fetch_all("SELECT * FROM stores ORDER BY name")


# PRICE COMPARISON

@app.post("/prices")
def create_price(price: PriceCreate):
    if not database.fetch_one(
        "SELECT id FROM products WHERE id = ?", (price.product_id,)
    ):
        raise HTTPException(404, "Product not found")

    if not database.fetch_one(
        "SELECT id FROM stores WHERE id = ?", (price.store_id,)
    ):
        raise HTTPException(404, "Store not found")

    price_id = database.execute("""
        INSERT INTO prices(product_id, store_id, price, price_date)
        VALUES (?, ?, ?, ?)
    """, (
        price.product_id,
        price.store_id,
        price.price,
        date.today().isoformat()
    ))

    return {"message": "Price saved", "id": price_id}


@app.get("/prices/{product_id}")
def compare_prices(product_id: int):
    product = database.fetch_one(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    )

    if not product:
        raise HTTPException(404, "Product not found")

    prices = database.fetch_all("""
        SELECT stores.name AS store,
               prices.price,
               prices.price_date
        FROM prices
        JOIN stores ON stores.id = prices.store_id
        WHERE prices.product_id = ?
        ORDER BY prices.price ASC
    """, (product_id,))

    return {
        "product": product["name"],
        "prices": prices,
        "cheapest": prices[0] if prices else None
    }


# SHOPPING LIST

@app.post("/shopping-list")
def add_shopping_item(item: ShoppingItemCreate):
    if not database.fetch_one(
        "SELECT id FROM products WHERE id = ?", (item.product_id,)
    ):
        raise HTTPException(404, "Product not found")

    item_id = database.execute("""
        INSERT INTO shopping_list(product_id, quantity)
        VALUES (?, ?)
    """, (item.product_id, item.quantity))

    return {"message": "Added to shopping list", "id": item_id}


@app.get("/shopping-list")
def get_shopping_list():
    return database.fetch_all("""
        SELECT shopping_list.id,
               products.name,
               shopping_list.quantity,
               products.unit,
               shopping_list.purchased
        FROM shopping_list
        JOIN products ON products.id = shopping_list.product_id
    """)


@app.put("/shopping-list/{item_id}/purchase")
def mark_purchased(item_id: int):
    with database.connect() as db:
        cursor = db.execute(
            "UPDATE shopping_list SET purchased = 1 WHERE id = ?",
            (item_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(404, "Shopping item not found")

    return {"message": "Item marked as purchased"}


@app.delete("/shopping-list/{item_id}")
def delete_shopping_item(item_id: int):
    with database.connect() as db:
        cursor = db.execute(
            "DELETE FROM shopping_list WHERE id = ?", (item_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(404, "Shopping item not found")

    return {"message": "Shopping item deleted"}


# BUDGET

@app.post("/budget")
def set_budget(budget: BudgetCreate):
    database.execute("""
        INSERT INTO budgets(amount, month)
        VALUES (?, ?)
        ON CONFLICT(month)
        DO UPDATE SET amount = excluded.amount
    """, (budget.amount, budget.month))

    return {"message": "Budget saved"}


@app.get("/budget/{month}")
def get_budget(month: str):
    budget = database.fetch_one(
        "SELECT * FROM budgets WHERE month = ?", (month,)
    )

    if not budget:
        raise HTTPException(404, "Budget not found")

    expenses = database.fetch_one("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE substr(expense_date, 1, 7) = ?
    """, (month,))

    spent = expenses["total"]

    return {
        "month": month,
        "budget": budget["amount"],
        "spent": spent,
        "remaining": budget["amount"] - spent
    }


# EXPENSES

@app.post("/expenses")
def create_expense(expense: ExpenseCreate):
    expense_id = database.execute("""
        INSERT INTO expenses(description, amount, expense_date)
        VALUES (?, ?, ?)
    """, (
        expense.description,
        expense.amount,
        date.today().isoformat()
    ))

    return {"message": "Expense saved", "id": expense_id}


@app.get("/expenses")
def get_expenses():
    return database.fetch_all(
        "SELECT * FROM expenses ORDER BY expense_date DESC"
    )


# RECIPES

@app.post("/recipes")
def create_recipe(recipe: RecipeCreate):
    recipe_id = database.execute("""
        INSERT INTO recipes(name, instructions, preparation_time)
        VALUES (?, ?, ?)
    """, (
        recipe.name,
        recipe.instructions,
        recipe.preparation_time
    ))

    return {"message": "Recipe created", "id": recipe_id}


@app.get("/recipes")
def get_recipes():
    return database.fetch_all("SELECT * FROM recipes ORDER BY name")


# PANTRY

@app.post("/pantry")
def add_pantry_item(item: PantryCreate):
    if not database.fetch_one(
        "SELECT id FROM products WHERE id = ?", (item.product_id,)
    ):
        raise HTTPException(404, "Product not found")

    item_id = database.execute("""
        INSERT INTO pantry(product_id, quantity, expiry_date)
        VALUES (?, ?, ?)
    """, (item.product_id, item.quantity, item.expiry_date))

    return {"message": "Pantry item added", "id": item_id}


@app.get("/pantry")
def get_pantry():
    return database.fetch_all("""
        SELECT pantry.id, products.name,
               pantry.quantity, products.unit, pantry.expiry_date
        FROM pantry
        JOIN products ON products.id = pantry.product_id
        ORDER BY pantry.expiry_date
    """)


@app.get("/pantry/expiration-alerts")
def expiration_alerts():
    return database.fetch_all("""
        SELECT products.name, pantry.quantity, pantry.expiry_date
        FROM pantry
        JOIN products ON products.id = pantry.product_id
        WHERE pantry.expiry_date IS NOT NULL
          AND pantry.expiry_date <= date('now', '+7 days')
        ORDER BY pantry.expiry_date
    """)


# MEAL PLANNER

@app.post("/meal-plans")
def create_meal_plan(plan: MealPlanCreate):
    if not database.fetch_one(
        "SELECT id FROM recipes WHERE id = ?", (plan.recipe_id,)
    ):
        raise HTTPException(404, "Recipe not found")

    if plan.meal_type not in ["Breakfast", "Lunch", "Dinner"]:
        raise HTTPException(400, "Invalid meal type")

    plan_id = database.execute("""
        INSERT INTO meal_plans(recipe_id, plan_date, meal_type)
        VALUES (?, ?, ?)
    """, (plan.recipe_id, plan.plan_date, plan.meal_type))

    return {"message": "Meal planned", "id": plan_id}


@app.get("/meal-plans")
def get_meal_plans():
    return database.fetch_all("""
        SELECT meal_plans.id, recipes.name,
               meal_plans.plan_date, meal_plans.meal_type
        FROM meal_plans
        JOIN recipes ON recipes.id = meal_plans.recipe_id
        ORDER BY meal_plans.plan_date
    """)


# SPECIAL OFFERS

@app.post("/offers")
def create_offer(offer: OfferCreate):
    for table, record_id in [
        ("products", offer.product_id),
        ("stores", offer.store_id)
    ]:
        if not database.fetch_one(
            f"SELECT id FROM {table} WHERE id = ?", (record_id,)
        ):
            raise HTTPException(404, f"{table.title()} not found")

    offer_id = database.execute("""
        INSERT INTO offers(product_id, store_id, discount_price, expiry_date)
        VALUES (?, ?, ?, ?)
    """, (
        offer.product_id,
        offer.store_id,
        offer.discount_price,
        offer.expiry_date
    ))

    return {"message": "Offer created", "id": offer_id}


@app.get("/offers")
def get_offers():
    return database.fetch_all("""
        SELECT products.name AS product,
               stores.name AS store,
               offers.discount_price,
               offers.expiry_date
        FROM offers
        JOIN products ON products.id = offers.product_id
        JOIN stores ON stores.id = offers.store_id
        WHERE offers.expiry_date IS NULL
           OR offers.expiry_date >= date('now')
        ORDER BY offers.discount_price
    """)


# ANALYTICS

@app.get("/analytics")
def analytics():
    month = date.today().strftime("%Y-%m")

    stats = {
        "products": "products",
        "stores": "stores",
        "recipes": "recipes",
        "pantry_items": "pantry",
        "shopping_items": "shopping_list",
        "expenses": "expenses",
        "offers": "offers",
        "meal_plans": "meal_plans"
    }

    result = {}

    for name, table in stats.items():
        record = database.fetch_one(
            f"SELECT COUNT(*) AS total FROM {table}"
        )
        result[name] = record["total"]

    expenses = database.fetch_one("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE substr(expense_date, 1, 7) = ?
    """, (month,))

    result["monthly_spending"] = expenses["total"]

    return result

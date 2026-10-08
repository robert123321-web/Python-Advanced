from fastapi import FastAPI, HTTPException
from database import create_tables, get_connection
from models import Category, CategoryCreate, Recipe, RecipeCreate

app = FastAPI(title="Online Recipe Book API")

create_tables()


@app.get("/")
def home():
    return {"message": "Online Recipe Book API is running"}


# -------------------- CATEGORIES --------------------

@app.get("/categories", response_model=list[Category])
def get_categories():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, name FROM categories ORDER BY id"
    ).fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, name FROM categories WHERE id = ?",
        (category_id,)
    ).fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return dict(row)


@app.post("/categories", response_model=Category, status_code=201)
def create_category(category: CategoryCreate):
    conn = get_connection()

    try:
        cursor = conn.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (category.name,)
        )
        conn.commit()

        category_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, name FROM categories WHERE id = ?",
            (category_id,)
        ).fetchone()

        return dict(row)

    except Exception as e:
        conn.rollback()
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )
        raise HTTPException(status_code=500, detail="Could not create category")

    finally:
        conn.close()


@app.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate):
    conn = get_connection()

    existing = conn.execute(
        "SELECT id FROM categories WHERE id = ?",
        (category_id,)
    ).fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found")

    try:
        conn.execute(
            "UPDATE categories SET name = ? WHERE id = ?",
            (category.name, category_id)
        )
        conn.commit()

        row = conn.execute(
            "SELECT id, name FROM categories WHERE id = ?",
            (category_id,)
        ).fetchone()

        return dict(row)

    except Exception:
        conn.rollback()
        raise HTTPException(
            status_code=400,
            detail="Category name already exists"
        )

    finally:
        conn.close()


@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    conn = get_connection()

    existing = conn.execute(
        "SELECT id FROM categories WHERE id = ?",
        (category_id,)
    ).fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found")

    conn.execute(
        "DELETE FROM categories WHERE id = ?",
        (category_id,)
    )
    conn.commit()
    conn.close()

    return {"message": "Category deleted successfully"}


# -------------------- RECIPES --------------------

@app.get("/recipes", response_model=list[Recipe])
def get_recipes():
    conn = get_connection()
    rows = conn.execute("""
        SELECT id, title, ingredients, instructions, category_id
        FROM recipes
        ORDER BY id
    """).fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int):
    conn = get_connection()
    row = conn.execute("""
        SELECT id, title, ingredients, instructions, category_id
        FROM recipes
        WHERE id = ?
    """, (recipe_id,)).fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return dict(row)


@app.post("/recipes", response_model=Recipe, status_code=201)
def create_recipe(recipe: RecipeCreate):
    conn = get_connection()

    category = conn.execute(
        "SELECT id FROM categories WHERE id = ?",
        (recipe.category_id,)
    ).fetchone()

    if category is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found")

    cursor = conn.execute("""
        INSERT INTO recipes
        (title, ingredients, instructions, category_id)
        VALUES (?, ?, ?, ?)
    """, (
        recipe.title,
        recipe.ingredients,
        recipe.instructions,
        recipe.category_id
    ))

    conn.commit()
    recipe_id = cursor.lastrowid

    row = conn.execute("""
        SELECT id, title, ingredients, instructions, category_id
        FROM recipes
        WHERE id = ?
    """, (recipe_id,)).fetchone()

    conn.close()

    return dict(row)


@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: RecipeCreate):
    conn = get_connection()

    existing = conn.execute(
        "SELECT id FROM recipes WHERE id = ?",
        (recipe_id,)
    ).fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Recipe not found")

    category = conn.execute(
        "SELECT id FROM categories WHERE id = ?",
        (recipe.category_id,)
    ).fetchone()

    if category is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found")

    conn.execute("""
        UPDATE recipes
        SET title = ?, ingredients = ?, instructions = ?, category_id = ?
        WHERE id = ?
    """, (
        recipe.title,
        recipe.ingredients,
        recipe.instructions,
        recipe.category_id,
        recipe_id
    ))

    conn.commit()

    row = conn.execute("""
        SELECT id, title, ingredients, instructions, category_id
        FROM recipes
        WHERE id = ?
    """, (recipe_id,)).fetchone()

    conn.close()

    return dict(row)


@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    conn = get_connection()

    existing = conn.execute(
        "SELECT id FROM recipes WHERE id = ?",
        (recipe_id,)
    ).fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Recipe not found")

    conn.execute(
        "DELETE FROM recipes WHERE id = ?",
        (recipe_id,)
    )
    conn.commit()
    conn.close()

    return {"message": "Recipe deleted successfully"}

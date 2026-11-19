
import sqlite3
from pathlib import Path

DATABASE_NAME = Path(__file__).resolve().parent.parent / "smartbasket.db"


def connect():
    db = sqlite3.connect(DATABASE_NAME)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def initialize_database():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            unit TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT
        );

        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            store_id INTEGER NOT NULL,
            price REAL NOT NULL,
            price_date TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(store_id) REFERENCES stores(id)
        );

        CREATE TABLE IF NOT EXISTS shopping_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            purchased INTEGER DEFAULT 0,
            FOREIGN KEY(product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            month TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            expense_date TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            instructions TEXT,
            preparation_time INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS pantry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            expiry_date TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS meal_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            plan_date TEXT NOT NULL,
            meal_type TEXT NOT NULL,
            FOREIGN KEY(recipe_id) REFERENCES recipes(id)
        );

        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            store_id INTEGER NOT NULL,
            discount_price REAL NOT NULL,
            expiry_date TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(store_id) REFERENCES stores(id)
        );
        """)


def execute(query, parameters=()):
    with connect() as db:
        cursor = db.execute(query, parameters)
        return cursor.lastrowid


def fetch_all(query, parameters=()):
    with connect() as db:
        return [dict(row) for row in db.execute(query, parameters).fetchall()]


def fetch_one(query, parameters=()):
    with connect() as db:
        row = db.execute(query, parameters).fetchone()
        return dict(row) if row else None

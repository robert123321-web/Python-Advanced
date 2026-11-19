"""SmartBasket - website frontend in pure Python (NiceGUI).

Install:  pip install nicegui requests
Backend:  (Personal Project folder)  python -m uvicorn app.main:app --reload --reload-dir app
Website:  (frontend folder)          python web.py      ->  http://localhost:8080

Product, store and banner photos are real photos looked up from Wikipedia by name.
"""
import csv
import datetime
import io
import os
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from functools import lru_cache
from urllib.parse import quote

import requests
from nicegui import ui

API = os.getenv("SMARTBASKET_API", "http://127.0.0.1:8000")
HEADERS = {"User-Agent": "SmartBasket/1.0 (student project)"}

NAV = [("Home", "/"), ("Products", "/products"), ("Stores", "/stores"),
       ("Compare prices", "/compare"), ("Shopping list", "/list")]
CATEGORIES = {
    "Fruit": ["apple", "banana", "orange", "lemon", "grape", "berry", "mango", "melon", "pear", "peach", "fruit"],
    "Vegetables": ["tomato", "potato", "carrot", "onion", "lettuce", "salad", "cucumber", "pepper", "broccoli", "garlic", "veg"],
    "Dairy": ["milk", "cheese", "yogurt", "yoghurt", "butter", "egg", "cream", "dairy"],
    "Bakery": ["bread", "bun", "cake", "croissant", "flour", "pastry", "bakery"],
    "Drinks": ["juice", "water", "cola", "coffee", "tea", "soda", "beer", "wine", "drink"],
    "Meat & fish": ["chicken", "beef", "meat", "fish", "pork", "sausage", "ham", "salmon", "tuna"],
}
FALLBACK = {"Fruit": "Fruit", "Vegetables": "Vegetable", "Dairy": "Dairy product", "Bakery": "Bread",
            "Drinks": "Drink", "Meat & fish": "Meat", "Other": "Grocery store"}
STORE_PHOTOS = ["Supermarket", "Grocery store", "Farmers' market", "Convenience store", "Hypermarket"]
TIPS = ["Prices change by store. Compare before you buy.",
        "Store brands often save 20% or more.",
        "Shop with a list. It cuts impulse buys.",
        "Fresh produce is cheapest when it's in season."]


# ───────────── API + data helpers ─────────────
def api(path):
    try:
        r = requests.get(f"{API}{path}", timeout=6)
        r.raise_for_status()
        data = r.json()
    except Exception:
        ui.notify(f"Could not load {path}", type="negative")
        return []
    if isinstance(data, dict):
        data = next((v for v in data.values() if isinstance(v, list)), [data])
    return data


def send(method, path, payload=None):
    r = requests.request(method, f"{API}{path}", json=payload, timeout=6)
    r.raise_for_status()


def pretty(k):
    return k.replace("_", " ").title()


def name_of(row):
    for k in ("name", "title", "product_name", "store_name"):
        if k in row:
            return str(row[k])
    return str(next((v for k, v in row.items() if k != "id"), row.get("id", "")))


def money_key(rows):
    for k, v in rows[0].items():
        if isinstance(v, (int, float)) and not isinstance(v, bool) and any(w in k.lower() for w in ("price", "cost", "total")):
            return k
    return None


def category_of(row):
    text = " ".join(str(row.get(k, "")).lower() for k in ("name", "title", "product_name", "category", "type"))
    for cat, words in CATEGORIES.items():
        for w in words:
            if w in text:
                return cat, w
    return "Other", None


# ───────────── Real photos (Wikipedia) ─────────────
@lru_cache(maxsize=1024)
def wiki_image(term, big=False):
    try:
        r = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/" + quote(term.replace(" ", "_")),
                         headers=HEADERS, timeout=6)
        if r.status_code != 200:
            return None
        d = r.json()
        if d.get("type") == "disambiguation":
            return None
        img = d.get("originalimage") if big else d.get("thumbnail")
        if big and img and img.get("width", 0) > 3500:
            img = d.get("thumbnail")
        return img["source"] if img else None
    except Exception:
        return None


@lru_cache(maxsize=1024)
def product_photo(name, cat, keyword):
    for term in dict.fromkeys([name, name.title(), name.rstrip("s"), keyword or name]):
        url = wiki_image(term)
        if url:
            return url
    return wiki_image(FALLBACK[cat]) or wiki_image("Grocery store")


def photos_for(rows):
    def one(row):
        cat, kw = category_of(row)
        return product_photo(name_of(row), cat, kw)
    with ThreadPoolExecutor(8) as pool:
        return list(pool.map(one, rows))


# ───────────── Page frame (header, content width, footer) ─────────────
@contextmanager
def frame(active):
    ui.colors(primary="#2E9E6B")
    ui.query("body").classes("bg-gray-50")
    with ui.header().classes("bg-white text-gray-800 shadow-sm items-center px-6 gap-2"):
        ui.label("🛒 SmartBasket").classes("text-xl font-bold text-primary mr-6")
        for title, path in NAV:
            ui.link(title, path).classes(
                "no-underline px-3 py-1 rounded-full " +
                ("bg-green-100 text-primary font-bold" if title == active else "text-gray-600 hover:bg-gray-100"))
    try:
        requests.get(f"{API}/health", timeout=3)
        online = True
    except requests.RequestException:
        online = False
    with ui.column().classes("w-full max-w-6xl mx-auto p-6 pb-20 gap-6"):
        if not online:
            ui.label("The server isn't reachable. Start the backend, then reload this page.") \
                .classes("w-full bg-red-100 text-red-800 p-4 rounded-lg")
        yield
    with ui.footer().classes("bg-white text-gray-500 justify-center text-sm"):
        ui.label("SmartBasket · Personal Project · Photos from Wikipedia")


def heading(title, subtitle):
    ui.label(title).classes("text-3xl font-bold")
    ui.label(subtitle).classes("text-gray-500 -mt-4")


def stat(icon, label, value):
    with ui.card().classes("flex-1 min-w-48 items-center py-6"):
        ui.icon(icon, size="2rem").classes("text-primary")
        ui.label(str(value)).classes("text-3xl font-bold")
        ui.label(label).classes("text-gray-500")


def empty_state(text, button=None, on_click=None):
    with ui.card().classes("w-full items-center py-12 gap-3"):
        ui.icon("shopping_basket", size="4rem").classes("text-gray-300")
        ui.label(text).classes("text-gray-500 text-lg")
        if button:
            ui.button(button, icon="add", on_click=on_click)


# ───────────── Dialogs ─────────────
def get_schema(path):
    spec = requests.get(f"{API}/openapi.json", timeout=6).json()
    s = spec["paths"][path]["post"]["requestBody"]["content"]["application/json"]["schema"]
    return spec["components"]["schemas"][s["$ref"].split("/")[-1]] if "$ref" in s else s


def ftype(p):
    if "type" in p:
        return p["type"]
    return next((o["type"] for o in p.get("anyOf", []) if o.get("type") not in (None, "null")), "string")


def add_dialog(path, title):
    try:
        schema = get_schema(path)
    except Exception:
        ui.notify("Could not load the form from the server", type="negative")
        return
    required, fields = schema.get("required", []), {}
    with ui.dialog() as dialog, ui.card().classes("w-96 gap-2"):
        ui.label(title).classes("text-xl font-bold")
        for name, p in schema.get("properties", {}).items():
            label, kind, d = pretty(name) + (" *" if name in required else ""), ftype(p), p.get("default")
            if kind in ("integer", "number"):
                el = ui.number(label, value=d or 0, format="%d" if kind == "integer" else "%.2f")
            elif kind == "boolean":
                el = ui.checkbox(label, value=bool(d))
            else:
                el = ui.input(label, value=str(d or ""))
            el.classes("w-full")
            fields[name] = (kind, el)

        def save():
            payload = {}
            for n, (kind, el) in fields.items():
                v = el.value
                if kind == "integer":
                    v = int(v or 0)
                elif kind == "number":
                    v = float(v or 0)
                elif kind != "boolean" and v in (None, "") and n not in required:
                    continue
                payload[n] = v
            try:
                send("POST", path, payload)
            except requests.HTTPError as e:
                ui.notify(f"Error: {e.response.text}", type="negative")
                return
            except Exception as e:
                ui.notify(f"Error: {e}", type="negative")
                return
            dialog.close()
            ui.notify("Saved!", type="positive")
            ui.navigate.reload()

        with ui.row().classes("w-full justify-end"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Save", on_click=save)
    dialog.open()


def delete_dialog(pid, name):
    with ui.dialog() as dialog, ui.card():
        ui.label(f"Delete {name}? This can't be undone.")

        def go():
            try:
                send("DELETE", f"/products/{pid}")
            except Exception as e:
                ui.notify(f"Error: {e}", type="negative")
                return
            dialog.close()
            ui.notify("Product deleted", type="warning")
            ui.navigate.reload()

        with ui.row().classes("w-full justify-end"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Delete", color="red", on_click=go)
    dialog.open()


# ───────────── Product card (shared) ─────────────
def product_card(row, photo, actions=True):
    cat, _ = category_of(row)
    with ui.card().classes("p-0 overflow-hidden hover:shadow-xl transition-shadow w-full"):
        if photo:
            ui.image(photo).classes("h-44 w-full")
        with ui.column().classes("p-4 gap-1 w-full"):
            ui.label(name_of(row)).classes("text-lg font-bold")
            ui.badge(cat).props("color=green-2 text-color=green-9")
            for k, v in row.items():
                if k not in ("id", "name", "title", "product_name") and v not in (None, ""):
                    ui.label(f"{pretty(k)}: {v}").classes("text-sm text-gray-500")
            if actions and "id" in row:
                with ui.row().classes("w-full justify-between mt-2"):
                    ui.button("Compare prices", icon="sell",
                              on_click=lambda r=row: ui.navigate.to(f"/compare?pid={r['id']}")).props("flat dense")
                    ui.button(icon="delete", on_click=lambda r=row: delete_dialog(r["id"], name_of(r))) \
                        .props("flat dense color=red")


# ───────────── Pages ─────────────
@ui.page("/")
def home():
    with frame("Home"):
        hero = wiki_image("Supermarket", True) or wiki_image("Grocery store", True)

        def hero_text():
            ui.label("Shop smarter. Spend less.").classes("text-5xl font-bold text-center")
            ui.label("Compare grocery prices across stores and build your cheapest shopping list.") \
                .classes("text-xl text-center max-w-2xl")
            with ui.row().classes("gap-3 mt-2"):
                ui.button("Compare prices", on_click=lambda: ui.navigate.to("/compare")) \
                    .props("size=lg color=white text-color=green-9")
                ui.button("Browse products", on_click=lambda: ui.navigate.to("/products")) \
                    .props("size=lg outline color=white")

        if hero:
            with ui.image(hero).classes("w-full h-96 rounded-2xl"):
                with ui.column().classes("absolute-full bg-black/55 items-center justify-center text-white gap-3"):
                    hero_text()
        else:
            with ui.column().classes("w-full h-96 rounded-2xl bg-green-600 items-center justify-center text-white gap-3"):
                hero_text()

        ui.label("💡 " + TIPS[datetime.date.today().toordinal() % len(TIPS)]) \
            .classes("w-full bg-green-50 text-green-900 p-4 rounded-lg")

        products, stores, slist = api("/products"), api("/stores"), api("/shopping-list")
        with ui.row().classes("w-full gap-4"):
            stat("inventory_2", "Products tracked", len(products))
            stat("storefront", "Stores", len(stores))
            stat("checklist", "On your list", len(slist))

        ui.label("How it works").classes("text-2xl font-bold mt-4")
        with ui.row().classes("w-full gap-4"):
            for icon, t, d in [("add_business", "1. Add stores", "Tell us where you shop."),
                               ("add_shopping_cart", "2. Add products", "List what you usually buy."),
                               ("sell", "3. Record prices", "We find the cheapest store for you.")]:
                with ui.card().classes("flex-1 min-w-56 gap-1"):
                    ui.icon(icon, size="2rem").classes("text-primary")
                    ui.label(t).classes("text-lg font-bold")
                    ui.label(d).classes("text-gray-500")

        with ui.row().classes("w-full gap-3"):
            ui.button("Add a store", icon="add_business", on_click=lambda: add_dialog("/stores", "Add a store")).props("outline")
            ui.button("Add a product", icon="add_shopping_cart", on_click=lambda: add_dialog("/products", "Add a product"))
            ui.button("Record a price", icon="sell", on_click=lambda: add_dialog("/prices", "Record a price")).props("outline")

        if products:
            ui.label("Latest products").classes("text-2xl font-bold mt-4")
            latest = products[-4:][::-1]
            imgs = photos_for(latest)
            with ui.element("div").classes("w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5"):
                for row, img in zip(latest, imgs):
                    product_card(row, img, actions=False)


@ui.page("/products")
def products_page():
    with frame("Products"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-0"):
                ui.label("Products").classes("text-3xl font-bold")
                ui.label("Everything you track.").classes("text-gray-500")
            ui.button("Add product", icon="add", on_click=lambda: add_dialog("/products", "Add a product"))

        rows = api("/products")
        if not rows:
            empty_state("No products yet. Add your first one!", "Add product",
                        lambda: add_dialog("/products", "Add a product"))
            return
        imgs = dict(zip([id(r) for r in rows], photos_for(rows)))
        state = {"q": "", "cat": "All"}

        @ui.refreshable
        def grid():
            shown = [r for r in rows
                     if state["q"].lower() in " ".join(str(v) for v in r.values()).lower()
                     and (state["cat"] == "All" or category_of(r)[0] == state["cat"])]
            ui.label(f"{len(shown)} of {len(rows)} products").classes("text-gray-500")
            if not shown:
                empty_state("Nothing matches your search.")
                return
            with ui.element("div").classes("w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5"):
                for r in shown:
                    product_card(r, imgs[id(r)])

        def change(key):
            def handler(e):
                state[key] = e.value or ("All" if key == "cat" else "")
                grid.refresh()
            return handler

        with ui.row().classes("w-full items-center gap-4"):
            ui.input(placeholder="Search products…", on_change=change("q")).props("outlined dense clearable") \
                .classes("w-72")
            ui.toggle(["All"] + list(CATEGORIES) + ["Other"], value="All", on_change=change("cat")).props("no-caps")
        grid()


@ui.page("/stores")
def stores_page():
    with frame("Stores"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-0"):
                ui.label("Stores").classes("text-3xl font-bold")
                ui.label("The shops you compare prices across.").classes("text-gray-500")
            ui.button("Add store", icon="add", on_click=lambda: add_dialog("/stores", "Add a store"))
        rows = api("/stores")
        if not rows:
            empty_state("No stores yet. Add the supermarkets you shop at.", "Add store",
                        lambda: add_dialog("/stores", "Add a store"))
            return
        with ui.element("div").classes("w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5"):
            for i, r in enumerate(rows):
                with ui.card().classes("p-0 overflow-hidden hover:shadow-xl transition-shadow w-full"):
                    photo = wiki_image(STORE_PHOTOS[i % len(STORE_PHOTOS)])
                    if photo:
                        ui.image(photo).classes("h-44 w-full")
                    with ui.column().classes("p-4 gap-1"):
                        ui.label(name_of(r)).classes("text-lg font-bold")
                        for k, v in r.items():
                            if k not in ("id", "name", "title", "store_name") and v not in (None, ""):
                                ui.label(f"{pretty(k)}: {v}").classes("text-sm text-gray-500")


@ui.page("/compare")
def compare_page(pid: str = ""):
    with frame("Compare prices"):
        heading("Compare prices", "Find the cheapest store for any product.")
        products = [p for p in api("/products") if "id" in p]
        if not products:
            empty_state("Add some products first, then record their prices.", "Add product",
                        lambda: add_dialog("/products", "Add a product"))
            return
        options = {p["id"]: name_of(p) for p in products}
        current = {"pid": int(pid) if pid.isdigit() and int(pid) in options else products[0]["id"]}

        @ui.refreshable
        def results():
            rows = api(f"/prices/{current['pid']}")
            if not rows:
                empty_state("No prices recorded for this product yet.", "Record a price",
                            lambda: add_dialog("/prices", "Record a price"))
                return
            mk = money_key(rows)
            if mk:
                lk = next((k for k in rows[0] if "store" in k.lower() and k != mk),
                          next((k for k, v in rows[0].items() if isinstance(v, str)), None))
                values = [r[mk] for r in rows]
                best, worst = min(values), max(values)
                with ui.row().classes("w-full gap-4"):
                    stat("trending_down", "Best price", f"{best:.2f}")
                    stat("functions", "Average", f"{sum(values) / len(values):.2f}")
                    stat("savings", "You save up to", f"{worst - best:.2f}")
                labels = [str(r.get(lk, i + 1)) for i, r in enumerate(rows)]
                ui.echart({
                    "grid": {"left": 110, "right": 30, "top": 10, "bottom": 30},
                    "tooltip": {},
                    "xAxis": {"type": "value"},
                    "yAxis": {"type": "category", "data": labels, "inverse": True},
                    "series": [{"type": "bar", "barWidth": 28,
                                "data": [{"value": v, "itemStyle": {"color": "#2E9E6B" if v == best else "#C5CED6",
                                                                    "borderRadius": [0, 8, 8, 0]}} for v in values]}],
                }).classes("w-full h-72 bg-white rounded-xl shadow p-2")
            columns = [{"name": k, "label": pretty(k), "field": k, "align": "left"} for k in rows[0]]
            ui.table(columns=columns, rows=rows).classes("w-full")

        with ui.row().classes("w-full items-center gap-4"):
            ui.select(options, value=current["pid"], label="Product",
                      on_change=lambda e: (current.update(pid=e.value), results.refresh())).classes("w-72")
            ui.button("Record a price", icon="add", on_click=lambda: add_dialog("/prices", "Record a price"))
        results()


@ui.page("/list")
def list_page():
    with frame("Shopping list"):
        heading("Shopping list", "Your list, built from the best prices.")
        rows = api("/shopping-list")
        if not rows:
            empty_state("Your list is empty. Record prices and it will fill up.", "Record a price",
                        lambda: add_dialog("/prices", "Record a price"))
            return
        mk = money_key(rows)
        with ui.row().classes("w-full gap-4"):
            stat("checklist", "Items", len(rows))
            if mk:
                stat("payments", "Estimated total", f"{sum(r[mk] for r in rows):.2f}")
        columns = [{"name": k, "label": pretty(k), "field": k, "align": "left"} for k in rows[0]]
        ui.table(columns=columns, rows=rows).classes("w-full")

        def download():
            buf = io.StringIO()
            w = csv.DictWriter(buf, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
            ui.download(buf.getvalue().encode("utf-8"), "shopping_list.csv")

        ui.button("Download as CSV", icon="download", on_click=download)


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="SmartBasket", favicon="🛒", port=8080, reload=False)
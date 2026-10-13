
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Online Recipe Book",
    page_icon="🍲",
    layout="wide"
)

st.title("🍲 Online Recipe Book")
st.caption("Manage recipes and categories in one place.")


def get_list(endpoint):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        st.error(f"Could not connect to the backend: {error}")
        return []


with st.sidebar:
    page = st.radio(
        "Navigation",
        ["Dashboard", "Manage Recipes", "Manage Categories"]
    )

categories = get_list("/categories")
recipes = get_list("/recipes")

category_names = {
    category["id"]: category["name"]
    for category in categories
}

if page == "Dashboard":
    st.header("Dashboard")

    col1, col2 = st.columns(2)
    col1.metric("Total Recipes", len(recipes))
    col2.metric("Total Categories", len(categories))

    st.subheader("All Recipes")

    if recipes:
        for recipe in recipes:
            category_name = category_names.get(
                recipe["category_id"],
                "Unknown category"
            )

            with st.expander(
                f'{recipe["title"]} — {category_name}'
            ):
                st.markdown("**Ingredients**")
                st.write(recipe["ingredients"])

                st.markdown("**Instructions**")
                st.write(recipe["instructions"])
    else:
        st.info("No recipes found.")

elif page == "Manage Recipes":
    st.header("Manage Recipes")
    st.info(
        "Your recipe list is loaded from FastAPI. "
        "We can add the create, edit, and delete forms next."
    )

    if recipes:
        st.dataframe(recipes, use_container_width=True)
    else:
        st.info("No recipes available yet.")

elif page == "Manage Categories":
    st.header("Manage Categories")

    if categories:
        st.dataframe(categories, use_container_width=True)
    else:
        st.info("No categories available yet.")

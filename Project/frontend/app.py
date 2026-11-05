from http.client import responses

import requests
import streamlit as st

API = "http://127.0.0.1:8000 "

st.set_page_config(page_title="My Book Library", page_icon="📚", layout="wide")

st.markdown(body="""
    <style>
        .stApp {background:#f6f8fb;}
        .block-container { max-width:1050px; padding-top:2rem}
        h1,h2,h3 {color: #20334b}
        div.stButton > button[kind="primary"] {background:#246b9c; border-radius:9px}
    </style>
""", unsafe_allow_html=True)


def api(method,path,data=None):
    try:
        headers={"X-API-Key":st.session_state.key}if st.session_state.key else{}
        response = requests.request(method,API + path,json=data,headers=headers,timeout=5)
        response.raise_for_status()
        return response.json()


with st.sidebar:
    st.title("📚 My Library")
    page = st.radio("Menu", ["Dashboard","Books","Authors"])
    st.divider()
    st.text_input("Api key", type="password", key="key")


books = api("GET","/books")
authors = api("GET","/authors")

names = {author["id"]: author["name"] for author in authors}


if page == "Dashboard":
    st.title("Welcome to my library")
    st.write("A simple page to organize your books and authors")

    a, b, c = st.columns(3)
    a.metric(label="total books", value=len(books))
    b.metric(label="Authors", value=len(authors))

    for book in books[-5:][::-1]:
        with st.container(border=True):
            st.write(f"**{book['title']}** -{names.get(books['authors_id'],"unlnown")})
elif page=

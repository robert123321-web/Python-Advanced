import streamlit as st

with st.form("my_form",clear_on_submit=True):
    name = st.text_input("Name")

    age = st.slider("Age",min_value=0,max_value=100)

    email = st.text_input("Email")

    biography = st.text_area("Short biio")

    terms = st.checkbox("I agree")
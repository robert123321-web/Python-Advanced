import pandas as pd
import streamlit as st
import plotly.express as px 


books_df = pd.read_cvs("bestsellers_with_categories_2022_03_27.csv")

st.title("Bestselling books")
st.write("This app analyzes the amazon yop drllinh books")

st.sidebar.heade("Add new book Data")


with st.sidebar.form("book_form"):
    new_name = st.text_input("Book name")
    new_author = st.text_input("Author")
    new_user_rating = st.slider("user Rating",0.0,5.0,0.0,0.1)
    new_reviews = st.number_input("Reviews", min_value=0,step=1)
    new_price = st.number_input("Price",min_val=0,step=1)
import streamlit as st
import requests
import pandas as pandas

st.title("Project managment App")

st.header("Add a Developer")
dev_name = st.text_input("Developer Name")
dev_experience = st.number_input("Experience (Years)", min_value=0,max_value=50,value=0)

if st.button("Create Developer"):
    dev_data={"name":dev_name,"experience":dev_experience}
    response = requests.post(json=dev_data)
    st.json(response.json())




st.header("Add a project")
proj_title = st.text_input("Project title")
proj_desc = st.text_input("Project description")
proj_langs = st.text_input("Languages Used(Coma-seperated)")
lead_dev_name = st.text_input("Developer Nme")
lead_dev_exp = st.number_input()


if st.button("Create Project"):
    dev_data={"name":dev_name,"experience":dev_experience}
    proj_data={
        "title":proj_title,
        "description":proj_desc.split(","),
        "lead_developer":lead_dev_data
    }
    response = requests.post(json=dev_data)
    st.json(response.json())



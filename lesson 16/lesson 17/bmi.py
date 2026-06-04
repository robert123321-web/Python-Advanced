pip install streamlit pandas

import streamlit as st
import pandas as pd

st.set_page_config(page_title="BMI Calculator", layout="centered")

# Initialize session state
if "people" not in st.session_state:
    st.session_state.people = []

st.title("BMI Calculator")

# Input form
name = st.text_input("Enter name:", value="Joe")

age = st.number_input(
    "Enter age:",
    min_value=1,
    max_value=120,
    value=24,
    step=1
)

weight = st.number_input(
    "Enter weight in kilograms:",
    min_value=1.0,
    value=85.0,
    step=0.1,
    format="%.2f"
)

height = st.number_input(
    "Enter height in meters:",
    min_value=0.5,
    value=1.80,
    step=0.01,
    format="%.2f"
)


def calculate_bmi(weight, height):
    return weight / (height ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"


if st.button("Add Person"):
    bmi = calculate_bmi(weight, height)
    category = bmi_category(bmi)

    st.session_state.people.append({
        "Name": name,
        "Age": age,
        "Weight (kg)": weight,
        "Height (m)": height,
        "BMI": round(bmi, 2),
        "Category": category
    })

    st.success(f"{name} has been added.")

# Results section
st.subheader("Results")

if st.session_state.people:
    for person in st.session_state.people:
        st.write(
            f"{person['Name']}, "
            f"Age: {person['Age']}, "
            f"Weight: {person['Weight (kg)']} kg, "
            f"Height: {person['Height (m)']} m, "
            f"BMI: {person['BMI']}, "
            f"Category: {person['Category']}"
        )

    st.divider()

    df = pd.DataFrame(st.session_state.people)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No people added yet.")
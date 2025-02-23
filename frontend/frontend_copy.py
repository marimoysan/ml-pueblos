import os
import streamlit as st
from streamlit_card import card
import pandas as pd

col1, col2 = st.columns(2)

with col1:
    with st.form("Form1"):
        flavor = st.selectbox("Select flavor", ["Vanilla", "Chocolate"], key="flav")
        intensity1 = st.slider(
            label="Select intensity", min_value=0, max_value=100, key="intens1"
        )
        submitted1 = st.form_submit_button("Submit 1")
    if submitted1:
        st.write(f"Form1 submitted. Flavor: {flavor} | Intensity: {intensity1}")

with col2:
    with st.form("Form2"):
        topping = st.selectbox("Select Topping", ["Almonds", "Sprinkles"], key="top")
        intensity2 = st.slider(
            label="Select Intensity", min_value=0, max_value=100, key="intens2"
        )
        submitted2 = st.form_submit_button("Submit 2")
    if submitted2:
        st.write(f"Form2 submitted. Topping: {topping} | Intensity: {intensity2}")

st.write("test")

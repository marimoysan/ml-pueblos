import os
import streamlit as st
from streamlit_card import card
import pandas as pd

cols = st.columns(2)


for idx, col in enumerate(cols):
    with col:
        with st.form(str(idx)):
            flavor = st.selectbox(
                "Select flavor", ["Vanilla", "Chocolate"], key=f"flav_{idx}"
            )
            intensity = st.slider(
                label="Select intensity",
                min_value=0,
                max_value=100,
                key=f"intens_{idx}",
            )
            submitted = st.form_submit_button(f"Submit {idx + 1}")
        if submitted:
            st.write(f"Form1 submitted. Flavor: {flavor} | Intensity: {intensity}")

# with col2:
#     with st.form("Form2"):
#         topping = st.selectbox("Select Topping", ["Almonds", "Sprinkles"], key="top")
#         intensity2 = st.slider(
#             label="Select Intensity", min_value=0, max_value=100, key="intens2"
#         )
#         submitted2 = st.form_submit_button("Submit 2")
#     if submitted2:
#         st.write(f"Form2 submitted. Topping: {topping} | Intensity: {intensity2}")

st.write("test")

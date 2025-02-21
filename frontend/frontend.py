import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the working directory to the script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

st.title('Pueblos')

st.write('''
# Explore different
''')

# Ensure the correct path to the CSV file
csv_path = '../data/output/pueblos.csv'

# Read the CSV file
df = pd.read_csv(csv_path)
st.line_chart(df['total_population'])
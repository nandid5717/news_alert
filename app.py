import streamlit as st
import pandas as pd
import os

DATA_FILE = "data.csv"

st.title("Debug App: Check CSV Columns")

if not os.path.exists(DATA_FILE):
    st.error(f"Data file {DATA_FILE} not found!")
else:
    try:
        df = pd.read_csv(DATA_FILE, sep=None, engine='python')
        st.write("### Columns in data.csv:")
        st.write(list(df.columns))
        st.write("### First 5 rows:")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error loading CSV: {e}")

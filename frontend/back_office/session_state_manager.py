import streamlit as st
import pandas as pd

# Define default values for your session state variables
default_session_state = {
    "df_select": pd.DataFrame(),
    "df_cat_columns": pd.DataFrame(),
    "df_train": pd.DataFrame(),
    "df_origin": pd.DataFrame(),
    "initial_run": True,
}


def initialize_session_state():
    # Initialize session state
    for key, value in default_session_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session_state():
    """Reset session state variables to their default values."""
    for key in default_session_state.keys():
        st.session_state[key] = default_session_state[key]

import streamlit as st
import welcome
import get_user_preferences
import get_user_preferences_map
import recommendations
import os


st.set_page_config(
    page_title="Pueblos",
    page_icon="🌾",
    initial_sidebar_state="expanded",
    layout= "wide",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))     


# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# Navigation logic
if st.session_state.page == "welcome":
    welcome.show()

elif st.session_state.page == "get_user_preferences_map":
    get_user_preferences_map.show()

elif st.session_state.page == "get_recommendations":
    recommendations.show()
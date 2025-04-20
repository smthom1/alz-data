from pathlib import Path
import streamlit as st
from PIL import Image
import os
from streamlit_extras.switch_page_button import switch_page

image_dir = Path("pics")

st.set_page_config(
    initial_sidebar_state="collapsed", layout="wide"
)


st.title("Welcome to the Happi!")

st.markdown("""
    <style>
        /* Hide sidebar */
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* Hide the collapsed sidebar toggle (arrow button) */
        div[data-testid="collapsedControl"] {
            display: none !important;
        }

        /* Adjust the main block to take full width */
        div[class*="main"] {
            margin-left: 0 !important;
        }

        /* Hide top menu hamburger if visible */
        header {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

if st.button("Start Intake"):
    st.markdown("<meta http-equiv='refresh' content='0; url=./intake'/>", unsafe_allow_html=True)

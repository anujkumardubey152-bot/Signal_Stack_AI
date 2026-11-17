
"""
Signal Stack AI
Main Streamlit application entry point.
"""

import streamlit as st

st.set_page_config(
    page_title="Signal Stack AI",
    page_icon="📊",
    layout="wide"
)

from modules.dashboard import render_dashboard

render_dashboard()

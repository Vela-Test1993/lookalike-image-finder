import homepage
import torch
import streamlit as st

homepage.setup_page()
homepage.search_tab()
st.link_button("Navigate to load data page",url="http://localhost:8501/load_data_page")

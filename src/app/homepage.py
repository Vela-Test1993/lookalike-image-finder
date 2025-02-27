import os
import sys
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src"))
sys.path.append(src_directory)
import streamlit as st
from utils import logger
from database_pinecone import querry_database
from model.clip_model import ClipModel

clip_model = ClipModel()
logger = logger.get_logger()

PAGE_TITLE = "Look A Like - Image Finder"
PAGE_LAYOUT = "centered"
SIDEBAR_TITLE = "Find Similar Images"

def setup_page():
    if 'is_page_configured' not in st.session_state:
        st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT)
        st.title(PAGE_TITLE)
        st.sidebar.title(SIDEBAR_TITLE)
        logger.info(f"Page configured with title '{PAGE_TITLE}', layout '{PAGE_LAYOUT}', and sidebar title '{SIDEBAR_TITLE}'")
        st.session_state.is_page_configured = True
    else:
        logger.info("Page configuration already completed. Skipping setup.")

def get_user_selection(options):
    selected_option = st.sidebar.selectbox("Select the option", options)
    return selected_option

def get_search_image_input():
    uploaded_image = st.sidebar.file_uploader("Upload the image to get similar images", type=['png', 'jpeg'])
    return uploaded_image

def get_search_text_input():
    user_search = st.sidebar.text_input("Enter the text to search")
    return user_search

def display_images(response):
    if response:
        cols = st.columns(2)
        for i, result in enumerate(response.matches):
            with cols[i % 2]:
                st.image(result.metadata["url"])

def write_message(message):
    st.write(message)

def get_images_by_text(query):
    embedding = clip_model.get_text_embedding(query)
    response = querry_database.fetch_data(embedding)
    message = f"Showing search results for {query}"
    write_message(message)
    images = display_images(response)

def get_images_by_image(query):
    embedding = clip_model.get_uploaded_image_embedding(query)
    response = querry_database.fetch_data(embedding)
    message = f"Showing search results of relevant images"
    write_message(message)
    images = display_images(response)

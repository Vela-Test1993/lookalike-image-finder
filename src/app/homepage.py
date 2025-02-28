import os
import sys
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src"))
sys.path.append(src_directory)
import streamlit as st
from utils import logger
from database_pinecone import querry_database,create_database
from model.clip_model import ClipModel
from data import data_set

clip_model = ClipModel()
logger = logger.get_logger()

PAGE_TITLE = "Look-a-Like: Image Finder"
PAGE_LAYOUT = "wide"
SIDEBAR_TITLE = "Find Similar Images"
PHOTO_ID_KEY = "photo_id" 
IMAGE_URL_KEY = "photo_image_url"
PINECONE_INDEX =  create_database.get_index()

def setup_page():
    st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT)
    st.markdown(f"""
        <h1 style='color:darkblue; text-align:center; font-size:32px; margin-top:-10px;'>
        <i>{PAGE_TITLE} 🔍📸</i>
        </h1>
        """, unsafe_allow_html=True)
    st.toast("✨ Welcome to Look-a-Like: The Ultimate Image Finder! Start searching now. 🔍")
    logger.info(f"Page successfully configured with title: {PAGE_TITLE}")

def search_tab():

    st.markdown("<hr>", unsafe_allow_html=True)  # To add a Horizontal line below title

    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None

    with st.container():

        col1, col2 = st.columns([7, 4], gap="small")
        with col1:
            search_query = st.text_input(
                label="🔍 Search for Images",
                placeholder="Type keywords (e.g., 'sunset beach', 'city skyline')",
                value=st.session_state.search_query
            )

            if search_query.strip() and search_query != st.session_state.search_query:
                st.session_state.search_query = search_query.strip()
                st.session_state.uploaded_image = None 

        with col2:
            uploaded_image = st.file_uploader(
                label="📤 Upload an Image",
                type=["png", "jpg", "jpeg"],
                help="Upload an image to find visually similar results."
            )

            if uploaded_image is not None and uploaded_image != st.session_state.uploaded_image:
                st.session_state.uploaded_image = uploaded_image
                st.session_state.search_query = "" 

        # with col3:
        #     st.markdown("<br>", unsafe_allow_html=True)
        #     if st.button(label="🗑️ Clear", help="Clear search input and uploaded image"):
        #         st.session_state.search_query = ""
        #         st.session_state.uploaded_image = None
        #         st.session_state.clear()

    with st.container():
        if st.session_state.search_query:
            get_images_by_text(st.session_state.search_query)
            st.session_state.search_query = "" 


        if st.session_state.uploaded_image:
            st.image(st.session_state.uploaded_image, caption="Uploaded Image", use_container_width=True)
            get_images_by_image(st.session_state.uploaded_image)
            st.session_state.uploaded_image = None
    
def get_user_selection(options):
    selected_option = st.sidebar.selectbox("Select the option", options)
    return selected_option

def get_search_image_input():
    uploaded_image = st.file_uploader("Upload the image to get similar images", type=['png', 'jpeg'])
    return uploaded_image

def get_search_text_input():
    user_search = st.sidebar.text_input("Enter the text to search")
    return user_search

def display_images(response):
    logger.info("Loading the images to dispay")
    if response:
        cols = st.columns(2)
        for i, result in enumerate(response.matches):
            with cols[i % 2]:
                st.image(result.metadata["url"], width=500)
        logger.info("Displayed the images successfully")

def write_message(message):
    st.write(message)

def get_images_by_text(query):
    embedding = clip_model.get_text_embedding(query)
    response = querry_database.fetch_data(embedding)
    message = f"🔍 Showing search results for {query}"
    write_message(message)
    images = display_images(response)

def get_images_by_image(query):
    embedding = clip_model.get_uploaded_image_embedding(query)
    response = querry_database.fetch_data(embedding)
    message = f"🔍 Showing search results of relevant images"
    write_message(message)
    images = display_images(response)

def load_data():
    st.sidebar.header("📊 Data Loading Parameters")
    start_index  = st.sidebar.number_input("Select start index", min_value=0, value=0)
    end_index  = st.sidebar.number_input("Select end index", min_value=0, value=100)

    if start_index > end_index:
        st.sidebar.error("⚠️ Start index must be earlier than the end index.")
        return
    
    if "load_clicked" not in st.session_state:
        st.session_state.load_clicked = False

    try:
        st.sidebar.info(f"Click the button to load data from index **{start_index} to {end_index}**.")
        if st.sidebar.button("🚀 Upsert Data", disabled=st.session_state.load_clicked, help="Click to insert data into the database"):
            st.session_state.load_clicked = True

            with st.spinner("⏳ Upserting data... Please wait"):
                df = data_set.get_df(start_index, end_index)
                if df.empty:
                    st.warning("⚠️ No data found in the selected range.")
                    return
                success_message = st.empty()
                progress_bar = st.progress(0)
                start = 0
                end = len(df)
                for i, data in df.iterrows():
                    create_database.process_and_upsert_data(PINECONE_INDEX, data, IMAGE_URL_KEY, PHOTO_ID_KEY)
                    success_message.success(f"Row {i + 1} (ID: {data.get('photo_id', 'unknown')}) added successfully!")
                    logger.info(f"Row {i + 1} (ID: {data.get('photo_id', 'unknown')}) upserted successfully.")
                    start = start + 1
                    progress = int((start) / end * 100)
                    progress_bar.progress(progress)
                progress_bar.empty()
                success_message.success("All data loaded and added to the database successfully!")
                st.session_state.load_clicked = False
                st.rerun()

    except Exception as e:
        st.error(f"Error loading data: {e}")
        logger.error(f"Error loading data: {e}")
        st.session_state.load_clicked = False


def about_us():
    if st.button("About us"):
        st.write("""
            This app allows you to search for images in two powerful ways:
    
            1. **Text-based Query**: You can simply type a description or keyword, and we will fetch the most relevant images from our database.
    
            2. **Image-based Query**: Alternatively, you can upload an image, and we'll search for similar images based on your input image.

            Whether you're looking for images based on a specific text query or searching using an image, our app makes it easy to find exactly what you're looking for. Simply enter your query and get results instantly!

            Explore and discover the images you need. Enjoy the search experience! 😊
            """)
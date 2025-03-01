import homepage
import torch

homepage.setup_page()
if homepage.get_or_greet_user_name():
    homepage.search_tab()
# st.link_button("Navigate to load data page",url="http://localhost:8501/load_data_page")

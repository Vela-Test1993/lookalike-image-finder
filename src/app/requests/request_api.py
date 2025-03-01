import os
import sys
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src"))
sys.path.append(src_directory)
from utils import logger
import requests

logger = logger.get_logger()

def get_api(end_point : str = None , query: str = 'Dog'):
    try:
        API_URL = f"http://127.0.0.1:8000/api/{end_point}"
        response = requests.post(API_URL, json={"query_text": query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e}")
        return []
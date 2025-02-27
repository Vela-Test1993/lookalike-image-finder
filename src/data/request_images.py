import requests
from PIL import Image
from utils import logger

logger = logger.get_logger()

def get_image_url(url):
    try:
        logger.info("Loading image from url to embed")
        res = requests.get(url,stream = True).raw
        img = Image.open(res)
        logger.info("Loaded the image to embed successfully")
        return img
    except Exception as e:
        logger.error(f"Unable to load the image to embed {e}")

def convert_image_to_embedding_format(query_image):
    try:
        logger.info("Loading the image to embed")
        image = Image.open(query_image)
        logger.info("Loaded the image to embed successfully")
        return image
    except Exception as e:
        logger.error(f"Unable to load the image to embed {e}")
import os
import sys
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src"))
sys.path.append(src_directory)
from pinecone import Pinecone, ServerlessSpec
import time
from model.clip_model import ClipModel
from config import config
from utils import logger
import pandas as pd

config = config.load_config()
logger = logger.get_logger()

clip_model = ClipModel()

def create_index(pinecone, index_name):
    pinecone.create_index(
    name=index_name,
    dimension=512,
    metric="cosine",
    spec=ServerlessSpec(
    cloud="aws",
    region="us-east-1"
        ) 
    )

def wait_till_index_loaded(pinecone, index_name):
    while True:
        index = pinecone.describe_index(index_name)
        if index.status.get("ready", False):
            index = pinecone.Index(index_name)
            logger.info(f"Index '{index_name}' is ready and is now accessible.")
            return index
        else:
            logger.debug(f"Index '{index_name}' is not ready yet. Checking again in 1 second.")
            time.sleep(1)

def get_index():
    try:
        pincone_api_key = config['pinecone_db']['pincone_api_key']
        pc = Pinecone(api_key=pincone_api_key)
        index = None
        index_name = "imagesearch"
        logger.info(f"Checking if the index '{index_name}' exists...")
        if not pc.has_index(index_name):
            logger.info(f"Index '{index_name}' does not exist. Creating a new index...")
            create_index(pc,index_name)
            logger.info(f"Index '{index_name}' creation initiated. Waiting for it to be ready...")
            index = wait_till_index_loaded(index_name,pc)
        else:
            index = pc.Index(index_name)
            logger.info(f"Index '{index_name}' already exists. Returning the existing index.")
        return index
    except Exception as e:
        logger.info(f"Error occurred while getting or creating the Pinecone index: {str(e)}", exc_info=True)
        return index
    
def process_and_upsert_data(index, data: pd.Series, url_key: str, id_key: str):
    """
    Processes a single row of data (pandas Series) by extracting the URL and ID, generating image embeddings using 
    a clip model, and then upserting the generated embeddings into a pinecone database index.

    This function handles:
    - Extracting the URL and ID from the provided `data` (a pandas Series) using the specified keys (`url_key` and `id_key`).
    - Using the `clip_model` to generate embeddings for the image found at the extracted URL.
    - Upserting the generated embeddings, along with the photo ID and URL, into the pinecone database index using the `upsert` method.

    Args:
        data (pandas.Series): A single row of data from the DataFrame, containing the URL and ID.
        url_key (str): The column name in the Series that contains the URL of the image.
        id_key (str): The column name in the Series that contains the photo ID.

    """
    # Validate if the required columns exist in the row (Series)
    if url_key not in data or id_key not in data:
        raise ValueError(f"Missing required keys: '{url_key}' or '{id_key}' in the data")

    try:
        logger.info("Started to process and upsert the data")
        url = data[url_key]
        photo_id = data[id_key]
        embeddings = clip_model.get_image_embedding(url)
        index.upsert(
            vectors=[{
                "id": photo_id,
                "values": embeddings,
                "metadata": {
                    "url": url,
                    "photo_id": photo_id
                }
            }],
            namespace="image-search-dataset",
        )
        logger.info(f"Successfully upserted data for photo_id {photo_id} with URL {url}")
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
    except Exception as e:
        logger.error(f"Error processing row with photo_id {data.get(id_key, 'unknown')}: {e}")
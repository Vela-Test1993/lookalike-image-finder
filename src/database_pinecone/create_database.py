import os
import sys
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src"))
sys.path.append(src_directory)
from pinecone import Pinecone, ServerlessSpec
import time
from model.clip_model import ClipModel
from data import request_images
from data import data_set
from config import config
from utils import logger

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
    
def upsert_data(index,embeddings,id,url):
    try :
        logger.info("Started to upsert the data")
        index.upsert(
            vectors=[{
                "id": id,
                "values": embeddings,
                "metadata": {
                "url": url,
                "photo_id": id
                }
            }],
            namespace="image-search-dataset",
        )
        logger.info(f"Successfully upserted the data in database")
    except Exception as e:
        logger.info(f"Unable to upsert the data {e}")
        raise
    
def add_data_to_database(df):
    try:
        index = get_index()
        logger.info("Starting to add the embeddings to the database")
        for _, data in df.iterrows():
            url = data['photo_image_url']
            id = data['photo_id']
            embeddings = clip_model.get_image_embedding(url)
            upsert_data(index,embeddings,id,url)
        logger.info("Added embeddings to the database successfully")
    except Exception as e:
        logger.info("Unable to add the data. Error : {e}")


# df = data_set.get_df(8000,8500)     
# add_data_to_database(df)
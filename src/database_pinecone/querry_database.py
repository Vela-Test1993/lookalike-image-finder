import os
import sys
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src"))
sys.path.append(src_directory)
from utils import logger
import streamlit as st
from model.clip_model import ClipModel
from database_pinecone import create_database

clip_model = ClipModel()
logger = logger.get_logger()

index = create_database.get_index()
namespace = 'image-search-dataset'

def fetch_data(embedding):
    try:
        response = index.query(
            top_k=10,
            vector=embedding,
            namespace=namespace,
            include_metadata=True)
        return response
    except Exception as e:
        raise

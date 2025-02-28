import os
import sys
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", "src"))
sys.path.append(src_directory)
from fastapi import APIRouter, HTTPException
from schemas import schema
from app import homepage


router = APIRouter()

@router.post("/{text_querry}", summary="Find the image by text")
def search_image(search_image: schema.ImageSearch):
    homepage.get_images_by_text(search_image.querry_text)

    
import os
import sys
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", "src"))
sys.path.append(src_directory)
from fastapi import APIRouter, HTTPException
from schemas.schema import ImageSearch
from app import homepage

router = APIRouter()

@router.post("/search", summary="Find images by text")
def search_image(search_request: ImageSearch):
    try:
        query = search_request.query_text.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query text cannot be empty")

        images = homepage.get_images_text_query(query)
        if not images:
            raise HTTPException(status_code=404, detail="No images found")

        return images

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
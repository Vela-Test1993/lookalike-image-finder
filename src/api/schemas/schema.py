from pydantic import BaseModel

class ImageSearch(BaseModel):
    query_text: str = "Dogs" 


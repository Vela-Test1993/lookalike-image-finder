import os
import sys
from transformers import AutoProcessor, CLIPModel, AutoTokenizer
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src"))
sys.path.append(src_directory)
from data import request_images
from utils import logger

logger = logger.get_logger()

class ClipModel:
    _models = {}

    def __init__(self, model_name: str = "openai/clip-vit-base-patch32", tokenizer_name: str = "openai/clip-vit-large-patch14"):
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name

        if model_name not in ClipModel._models:
            ClipModel._models[model_name] = self.load_models()

    def load_models(self):
        try:
            logger.info(f"Loading the models: {self.model_name}")
            model = CLIPModel.from_pretrained(self.model_name)
            processor = AutoProcessor.from_pretrained(self.model_name)
            tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name)
            return {
                'model': model,
                'processor': processor,
                'tokenizer': tokenizer
            }
        except Exception as e:
            logger.error(f"Unable to load the model {e}")
            raise

    def get_text_embedding(self, text: str):
        try:
            logger.info(f"Getting embedding for the text: {text}")
            inputs = self._models[self.model_name]['tokenizer']([text], padding=True, return_tensors="pt")
            text_features = self._models[self.model_name]['model'].get_text_features(**inputs)
            text_embedding = text_features.detach().numpy().flatten().tolist()
            logger.info("Text embedding successfully retrieved.")
            return text_embedding
        except Exception as e:
            logger.error(f"Error while getting embedding for text: {e}")
            raise

    def get_image_embedding(self, image):
        try:
            logger.info(f"Getting embedding for the image")
            image = request_images.get_image_url(image)
            inputs = self._models[self.model_name]['processor'](images=image, return_tensors="pt")
            image_features = self._models[self.model_name]['model'].get_image_features(**inputs)
            embeddings = image_features.detach().cpu().numpy().flatten().tolist()
            logger.info("Image embedding successfully retrieved.")
            return embeddings
        except Exception as e:
            logger.error(f"Error while getting embedding for image: {e}")
            raise
        
    def get_uploaded_image_embedding(self, image):
        try:
            logger.info(f"Getting embedding for the image")
            image = request_images.convert_image_to_embedding_format(image)
            inputs = self._models[self.model_name]['processor'](images=image, return_tensors="pt")
            image_features = self._models[self.model_name]['model'].get_image_features(**inputs)
            embeddings = image_features.detach().cpu().numpy().flatten().tolist()
            logger.info("Image embedding successfully retrieved.")
            return embeddings
        except Exception as e:
            logger.error(f"Error while getting embedding for image: {e}")
            raise

if __name__ == "__main__":
    try:
        logger.info("Starting the initialization of the ClipModel class...")
        clip_model = ClipModel()
        logger.info("ClipModel class initialized successfully.")
    except Exception as e:
        logger.error(f"Error during ClipModel initialization: {str(e)}")
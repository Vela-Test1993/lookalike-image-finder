import yaml
from utils import logger

logger = logger.get_logger()

def load_config():
    try:
        with open('config.yaml', 'r') as file:
            config_data = yaml.load(file, Loader=yaml.FullLoader)
            logger.info("Successfully loaded the config.")
            return config_data
    except Exception as e:
        logger.error(f"Unexpected error occurred while loading the config: {e}")
        raise Exception(f"Error loading configuration: {e}")

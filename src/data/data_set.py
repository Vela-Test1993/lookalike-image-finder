import pandas as pd
from utils import logger

logger = logger.get_logger()

file_name = 'src/data/image_dataset.csv'

tsv_file = 'src/data/photos.tsv000'

def convert_tsc_to_csv(tsv_file):
    df = pd.read_csv(tsv_file, sep='\t', header=0)
    dataset = df.to_csv(file_name)
    return dataset

def get_df(start_index,end_index):
    try:
        logger.info("Loading the dataframe")
        image_df = pd.read_csv(file_name)
        final_df = image_df[['photo_id','photo_image_url']]
        df = final_df[start_index:end_index]
        logger.info("Successfully loaded the data frame") 
        return df
    except Exception as e:
        logger.error(f"Unable to load the dataframe {e}")
        raise
    
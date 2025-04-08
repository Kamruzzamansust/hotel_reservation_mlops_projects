 # config.py
import pandas as pd 
import yaml
import os 
import pandas 
from src.logger import get_logger
from src.custom_exception import CustomException
import mlflow


logger = get_logger(__name__)

    

def read_yaml(config_path: str):
    try:
        if not isinstance(config_path, str) or not os.path.exists(config_path):
            raise ValueError("Provided config path must be a string path to a file")

        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    except Exception as e:
        raise CustomException("Failed to load configuration file", e)
    

def load_data(path):
    try:
        logger.info("Loading data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading the data {e}")
        raise CustomException("Failed to load data" , e)
        
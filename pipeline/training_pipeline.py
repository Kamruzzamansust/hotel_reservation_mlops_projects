import os
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_function import read_yaml
from config.paths_config import *

if __name__ == "__main__":
    # ✅ Get the dynamic config file path (no hardcoding)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "config", "config.yaml"))

    # ✅ Read config using your common_function
    config = read_yaml(CONFIG_FILE_PATH)

    # ✅ Step 1: Data Ingestion
    data_ingestion = DataIngestion(CONFIG_FILE_PATH)
    data_ingestion.run(table_name=config['database']['table_name'])

    # ✅ Step 2: Data Processing
    processor = DataProcessor(
        TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH
    )
    processor.process()

    # ✅ Step 3: Model Training
    trainer = ModelTraining(
        PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH
    )
    trainer.run()

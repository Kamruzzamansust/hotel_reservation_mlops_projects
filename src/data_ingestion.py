import os 
import pandas as pd 
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_function import read_yaml

logger = get_logger(__name__)

# -----------------------------
# DatabaseUploader Class
# -----------------------------
class DatabaseUploader:
    def __init__(self, config: dict):
        db_config = config.get("database", {})
        self.user = db_config.get("user")
        self.password = db_config.get("password")
        self.host = db_config.get("host")
        self.port = db_config.get("port")
        self.database = db_config.get("name")
        self.engine = self.create_engine()

    def create_engine(self):
        connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        return create_engine(connection_string)

    def load_csv_to_df(self, filepath: str) -> pd.DataFrame:
        return pd.read_csv(filepath)

    def upload_to_postgres(self, df: pd.DataFrame, table_name: str):
        df.to_sql(table_name, self.engine, if_exists="replace", index=False)
        print(f"✅ Data uploaded to '{table_name}' table successfully!")










# -----------------------------
# DataIngestion Class
# -----------------------------
class DataIngestion:
    def __init__(self, config_path: str):
        try:
            self.config = read_yaml(config_path)
            self.db_uploader = DatabaseUploader(self.config)
            self.raw_data_dir = RAW_FILE_PATH
            self.train_file_path = TRAIN_FILE_PATH
            self.test_file_path = TEST_FILE_PATH
            self.train_ratio = self.config.get("data_ingestion", {}).get("train_ratio", 0.8)

            os.makedirs(self.raw_data_dir, exist_ok=True)
            os.makedirs(os.path.dirname(self.train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.test_file_path), exist_ok=True)

            self.logger = get_logger(__name__)
        except Exception as e:
            raise CustomException(e)

    def fetch_and_store_data(self, table_name: str):
        try:
            query = f"SELECT * FROM {table_name};"
            df = pd.read_sql(query, self.db_uploader.engine)
            output_path = os.path.join(self.raw_data_dir, "raw_data.csv")
            df.to_csv(output_path, index=False)
            self.logger.info(f"✅ Data fetched from '{table_name}' and saved to RAW folder at: {output_path}")
            return df
        except Exception as e:
            self.logger.error("❌ Failed to fetch data from PostgreSQL and save to RAW folder!")
            raise CustomException(e)

    def split_and_store_data(self, df: pd.DataFrame):
        try:
            train_df, test_df = train_test_split(df, test_size=1-self.train_ratio, random_state=42)
            train_df.to_csv(self.train_file_path, index=False)
            test_df.to_csv(self.test_file_path, index=False)
            self.logger.info(f"✅ Train and test data saved to: {self.train_file_path}, {self.test_file_path}")
        except Exception as e:
            self.logger.error("❌ Failed to perform train-test split or save the data!")
            raise CustomException(e)

    def run_data_ingestion(self, table_name: str):
        df = self.fetch_and_store_data(table_name)
        self.split_and_store_data(df)

    def run(self, table_name: str):
        try:
            logger.info("🚀 Starting data ingestion process")
            self.run_data_ingestion(table_name)
        except Exception as e:
            self.logger.error("❌ Failed to start data ingestion process!")
            raise CustomException(e)

        logger.info("✅ Data ingestion process completed successfully")

# -----------------------------
# Usage
# -----------------------------
if __name__ == "__main__":
    config_path = "/home/kamruzaman/Learning/mlops_projects/hotel_reservation_prediction/config/config.yaml"
    csv_path = "/home/kamruzaman/Learning/mlops_projects/hotel_reservation_prediction/notebook/Hotel Reservations.csv"
    table_name = "hotel_reservation"

    # ✅ Step 1: Upload CSV to PostgreSQL (Optional — do only once)
    config = read_yaml(config_path)
    uploader = DatabaseUploader(config)
    df = uploader.load_csv_to_df(csv_path)
    uploader.upload_to_postgres(df, table_name)

    # ✅ Step 2 & 3 Combined: Full Ingestion Pipeline
    ingestion = DataIngestion(config_path)
    ingestion.run(table_name)


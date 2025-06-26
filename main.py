from src.textSummarizer.components.data_ingestion import DataIngestion,DataIngestionConfig
from src.textSummarizer.config.configuration import ConfigurationManager
from src.textSummarizer.constants import *


config = ConfigurationManager(config_path=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)


data_ingestion_config = config.get_data_ingestion_config()

di = DataIngestion(config=data_ingestion_config)
di.run()
from src.textSummarizer.components.data_ingestion import DataIngestion,DataIngestionConfig
from src.textSummarizer.components.data_transformation import DataTransformation,DataTransformationConfig
from src.textSummarizer.components.model_trainer import ModelTrainer,ModelTrainerConfig
from src.textSummarizer.config.configuration import ConfigurationManager
from src.textSummarizer.constants import *


config = ConfigurationManager(config_path=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)


# data_ingestion_config = config.get_data_ingestion_config()

# di = DataIngestion(config=data_ingestion_config)
# di.run()

# data_transformation_config= config.get_data_transformation_config()
# dt = DataTransformation(config=data_transformation_config)
# dt.run()

model_training_config = config.get_model_trainer_config()
mt = ModelTrainer(config=model_training_config)
mt.run()
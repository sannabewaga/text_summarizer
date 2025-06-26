import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Log file name with timestamp
LOG_FILE = os.path.join(LOGS_DIR, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Create and configure logger
logger = logging.getLogger("TextSummarizerLogger")
logger.setLevel(logging.DEBUG)  # can switch to INFO or WARNING in production

# Formatter
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# File Handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

# Stream (Console) Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# Avoid duplicate logs if already configured
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Optional: silence other noisy loggers (e.g., from transformers or urllib3)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)

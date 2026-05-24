import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger('network_sniffer')
logger.setLevel(logging.DEBUG)

log_file = os.path.join(LOG_DIR, 'sniffer.log')
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Optional: also output to console
console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)

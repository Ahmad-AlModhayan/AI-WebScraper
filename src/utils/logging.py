import logging
import sys
from logging.handlers import RotatingFileHandler
from src.utils.config import config
import os

def setup_logging():
    """
    Configure logging with multiple handlers and advanced formatting
    """
    # Create logger
    logger = logging.getLogger('ai_web_scraper')
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Ensure logs directory exists
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
        'logs'
    )
    os.makedirs(log_dir, exist_ok=True)
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(config.get('logging.console_level', logging.INFO))
    
    # File Handler with rotation
    log_file_path = os.path.join(log_dir, config.get('logging.file_name', 'app.log'))
    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=config.get('logging.max_file_size', 10*1024*1024),  # 10MB
        backupCount=config.get('logging.backup_count', 5)
    )
    file_handler.setLevel(config.get('logging.file_level', logging.DEBUG))
    
    # Formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Create a module-level logger
logger = setup_logging()

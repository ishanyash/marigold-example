# utils/logger.py

import logging
import os
from config.settings import LOG_LEVEL

def get_logger(name):
    """
    Configure and return a logger instance.
    
    Args:
        name: Name of the logger, typically __name__ from the calling module
        
    Returns:
        logging.Logger: Configured logger
    """
    # Set up logging
    logger = logging.getLogger(name)
    
    # Set log level from environment or default to INFO
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler if not already added
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
    
    return logger
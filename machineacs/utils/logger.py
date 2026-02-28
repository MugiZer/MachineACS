import logging
import sys
from pathlib import Path

def setup_logging(log_file: str = "pipeline.log", log_dir: str = "logs"):
    """
    Sets up a production-grade logger that outputs to both console and file.
    """
    # Create logs directory if it doesn't exist
    root_dir = Path(__file__).resolve().parent.parent
    log_path = root_dir / log_dir
    log_path.mkdir(exist_ok=True)
    
    file_path = log_path / log_file

    logger = logging.getLogger("machineacs")
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if function is called multiple times
    if logger.handlers:
        return logger

    # 1. File Handler (Detailed logs for debugging)
    file_handler = logging.FileHandler(file_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(file_format)

    # 2. Console Handler (Clean logs for user)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(message)s') # Keep it clean for CLI
    console_handler.setFormatter(console_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a singleton logger instance
logger = setup_logging()

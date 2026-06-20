import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path



def setup_logger():
    BASE_DIR = Path(__file__).resolve().parent
    logs_dir = BASE_DIR / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "blocks.log"

    logger = logging.getLogger("AI_Assistant")
    logger.setLevel(logging.DEBUG)

    file_handler = TimedRotatingFileHandler(
    log_file,
    when="midnight",  
    interval=1,
    backupCount=7,   
    encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger 
import logging

def setup_logger(logfile="firewall_audit.log"):
    logger = logging.getLogger("ContentFirewall")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(logfile)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger

def get_logger():
    logger = logging.getLogger("ContentFirewall")
    if not logger.handlers:
        setup_logger()
    return logger

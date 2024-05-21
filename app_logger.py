import logging
from config import LogConfiguration


def get_logger():
    log = logging.getLogger(LogConfiguration.logger_name)
    formatter = logging.Formatter(LogConfiguration.logger_formatter)
    handler = logging.FileHandler(filename=LogConfiguration.log_file_base_name)
    handler.setFormatter(formatter)
    log.setLevel('INFO')
    log.addHandler(handler)
    return log


logger = get_logger()

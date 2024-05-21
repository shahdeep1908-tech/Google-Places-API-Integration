class LogConfiguration:
    logger_name: str = "Google Places API"
    # The below format represents: timestamp of log, log level (INFO, ERROR, ...), name of logger, path of file where
    # error occurred, line number, function name, and the custom message we added
    logger_formatter: str = "%(asctime)s-%(levelname)s-%(name)s-%(process)d-%(pathname)s|%(lineno)s:: %(funcName)s|%(" \
                            "lineno)s:: %(message)s "
    # Name of file where logs will be created
    log_file_base_name: str = "logs"

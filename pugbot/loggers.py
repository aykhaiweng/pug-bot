import logging

from . import conf


# This will serve as the default logger
pugbot_logger = logging.getLogger('pugbot')
pugbot_logger.setLevel(conf.DEFAULT_LOG_LEVEL)

# Change the default log level for the root logger as well
root_logger = logging.getLogger('root')
root_logger.setLevel(conf.DEFAULT_LOG_LEVEL)


def log(message, level=None, logger=None, format=None, *args, **kwargs):
    """
    Helper function for controlling the logs
    """
    # Fallbacks
    logger = logger or pugbot_logger  # Fallback on the pugbot logger
    level = level or conf.DEFAULT_LOG_LEVEL  # Fallback on the debug level
    format = format or conf.DEFAULT_LOG_FORMATTER  # Fallback for the logging format

    # If no custom logger was specified, set up the defaults
    if 'logger' not in kwargs:
        ch = logging.StreamHandler()  # Console Handler
        ch.setLevel(level)
        ch.setFormatter(logging.Formatter(format))
        logger.addHandler(ch)

    return logger.log(level, message, *args, **kwargs)

import logging

from pugbot import conf

# Change the default log level for the root logger as well
root_logger = logging.getLogger('root')
root_logger.setLevel(conf.DEFAULT_LOG_LEVEL)
ch = logging.StreamHandler()  # Console Handler
ch.setLevel(root_logger.level)
ch.setFormatter(logging.Formatter(conf.DEFAULT_LOG_FORMATTER))
root_logger.addHandler(ch)
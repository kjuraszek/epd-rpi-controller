"""
Module contains logging related functions and variables
"""

import logging
import logging.config

from config import Config

logging.config.fileConfig(Config.CONFIG_FILE)
logger = logging.getLogger()

_LOGGERS = {
    "kafka": Config.KAFKA_LOGGING_LEVEL,
    "tornado": Config.TORNADO_LOGGING_LEVEL,
    "matplotlib": Config.MATPLOTLIB_LOGGING_LEVEL,
}


def configure_lib_loggers() -> None:
    """Function sets logging levels from config for external modules"""
    for log, level in _LOGGERS.items():
        lib_logger = logging.getLogger(log)
        lib_logger.setLevel(level)

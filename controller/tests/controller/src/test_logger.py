"""
Logger module tests
"""

import logging

from logger import logger, configure_lib_loggers

class TestLogger:
    def test_logger(self):
        root_logger = logging.getLogger('root')
        assert logger == root_logger
        assert logger.level == 20

    def test_configure_lib_loggers(self):
        configure_lib_loggers()
        kafka_logger = logging.getLogger('kafka')
        assert kafka_logger.level == 50
        matplotlib_logger = logging.getLogger('matplotlib')
        assert matplotlib_logger.level == 30
        tornado_logger = logging.getLogger('tornado')
        assert tornado_logger.level == 10

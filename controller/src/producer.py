"""Module exports Producer class"""

import time
import logging

from kafka import KafkaProducer

from waiting import wait, TimeoutExpired

from config import Config
from src.helpers import BaseThread

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Producer(BaseThread):
    """Producer is responsible for switching view within time interval."""

    def __init__(self) -> None:
        """Producer constructor method"""
        BaseThread.__init__(self)
        self.interval = Config.PRODUCER_INTERVAL
        self.order = 'next' if Config.PRODUCER_ASC_ORDER else 'prev'

    def stop(self) -> None:
        """Method stops the Producer"""
        self.stop_event.set()

    def run(self) -> None:
        """Main method which runs on Producer start

        Method triggers view change (previous or next) within time interval
        """

        producer = KafkaProducer(bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVER)
        time.sleep(self.interval)
        while not self.stop_event.is_set():
            producer.send(Config.KAFKA_VIEW_MANAGER_TOPIC, bytes(self.order, encoding='utf-8'))
            try:
                wait(lambda: self.stop_event.is_set(), timeout_seconds=self.interval)  # pylint: disable=W0108
            except TimeoutExpired:
                pass

        producer.close()

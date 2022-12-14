import threading
import time
import logging

from kafka import KafkaProducer

from waiting import wait, TimeoutExpired

from config import KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL, KAFKA_BOOTSTRAP_SERVER

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Producer(threading.Thread):
    '''
    kafka producer
    '''
    def __init__(self, asc_order = True):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.interval = PRODUCER_INTERVAL
        self.order = 'next' if asc_order else 'prev'

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER)
        time.sleep(self.interval)
        while not self.stop_event.is_set():
            producer.send(KAFKA_VIEW_MANAGER_TOPIC, bytes(self.order, encoding='utf-8'))
            try:
                wait(lambda : self.stop_event.is_set(), timeout_seconds=self.interval)
            except TimeoutExpired:
                pass
            else:
                break

        producer.close()

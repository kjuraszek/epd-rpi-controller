import threading
import logging

from kafka import KafkaConsumer

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Consumer(threading.Thread):
    '''
    kafka consumer
    '''
    def __init__(self, view_manager):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.view_manager = view_manager

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVER,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe([Config.KAFKA_VIEW_MANAGER_TOPIC])

        while not self.stop_event.is_set():
            for message in consumer:
                try:
                    message_decoded = message.value.decode('utf-8')
                    if message_decoded == 'prev':
                        self.prev()
                    elif message_decoded == 'next':
                        self.next()
                    elif message_decoded == 'stop':
                        self.stop()
                except Exception:  # pylint: disable=W0703
                    logger.error('Consumer decoding error with %s', message.value)
                if self.stop_event.is_set():
                    logger.info('Stopping consumer')
                    break

        consumer.close()

    def prev(self):
        self.view_manager.prev()

    def next(self):
        self.view_manager.next()

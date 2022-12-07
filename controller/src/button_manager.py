import threading
import time
import logging

from kafka import KafkaProducer

from waiting import wait, TimeoutExpired
import RPi.GPIO as GPIO

from config import KAFKA_VIEW_MANAGER_TOPIC, LEFT_BUTTON_PIN, RIGHT_BUTTON_PIN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ButtonManager(threading.Thread):
    '''
    button manager
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LEFT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def stop(self):
        self.stop_event.set()

    def run(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        GPIO.add_event_detect(LEFT_BUTTON_PIN, GPIO.FALLING,
                              callback=self._left_button_callback)
        GPIO.add_event_detect(RIGHT_BUTTON_PIN, GPIO.FALLING,
                              callback=self._right_button_callback)
        while not self.stop_event.is_set():
            try:
                wait(lambda : self.stop_event.is_set(), timeout_seconds=0.1)
            except TimeoutExpired:
                pass
            else:
                break

        self.producer.close()

    def _left_button_callback(self, *args):
        time.sleep(0.01)
        self.producer.send(KAFKA_VIEW_MANAGER_TOPIC, bytes('prev', encoding='utf-8'))

    def _right_button_callback(self, *args):
        time.sleep(0.01)
        self.producer.send(KAFKA_VIEW_MANAGER_TOPIC, bytes('next', encoding='utf-8'))


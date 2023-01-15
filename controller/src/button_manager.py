"""Module exports ButtonManager class"""

import threading
import time
import logging

from kafka import KafkaProducer

from waiting import wait, TimeoutExpired

from config import Config

# pylint: disable=R0402
if Config.USE_BUTTONS:
    import RPi.GPIO as GPIO
else:
    import Mock.GPIO as GPIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ButtonManager(threading.Thread):
    """ButtonManager controls physical buttons

    ButtonManager is responsible for switching the views
    basing on pressed physical buttons.
    """

    def __init__(self):
        """ButtonManager constructor method"""
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.producer = None
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Config.LEFT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(Config.RIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def stop(self):
        """Method stops the ButtonManager"""
        self.stop_event.set()

    def run(self):
        """Main method which runs on manager start

        Method detects events from buttons and triggers certain actions.
        """

        self.producer = KafkaProducer(bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVER)
        GPIO.add_event_detect(Config.LEFT_BUTTON_PIN, GPIO.FALLING,
                              callback=self._left_button_callback,
                              bouncetime=200)
        GPIO.add_event_detect(Config.RIGHT_BUTTON_PIN, GPIO.FALLING,
                              callback=self._right_button_callback,
                              bouncetime=200)
        while not self.stop_event.is_set():
            try:
                wait(lambda: self.stop_event.is_set(), timeout_seconds=0.1)  # pylint: disable=W0108
            except TimeoutExpired:
                pass
            else:
                break

        self.producer.close()

    def _left_button_callback(self, *args):  # pylint: disable=W0613
        """Callback for left button"""
        time.sleep(0.01)
        self.producer.send(Config.KAFKA_VIEW_MANAGER_TOPIC, bytes('prev', encoding='utf-8'))

    def _right_button_callback(self, *args):  # pylint: disable=W0613
        """Callback for right button"""
        time.sleep(0.01)
        self.producer.send(Config.KAFKA_VIEW_MANAGER_TOPIC, bytes('next', encoding='utf-8'))

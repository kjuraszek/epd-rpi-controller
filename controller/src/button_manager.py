"""Module exports ButtonManager class"""

import time
from typing import Any, Optional

from kafka import KafkaProducer

from waiting import wait, TimeoutExpired

from config import Config
from src.helpers import BaseThread

# pylint: disable=R0402
if Config.USE_BUTTONS:
    import RPi.GPIO as GPIO
else:
    import Mock.GPIO as GPIO


class ButtonManager(BaseThread):
    """ButtonManager controls physical buttons

    ButtonManager is responsible for switching the views
    basing on pressed physical buttons.
    """

    def __init__(self) -> None:
        """ButtonManager constructor method"""
        BaseThread.__init__(self)
        self.producer: Optional[KafkaProducer] = None
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Config.LEFT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(Config.RIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def stop(self) -> None:
        """Method stops the ButtonManager"""
        self.stop_event.set()

    def run(self) -> None:
        """Main method which runs on manager start

        Method detects events from buttons and triggers certain actions.
        """

        self.producer = KafkaProducer(bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVER)
        GPIO.add_event_detect(
            Config.LEFT_BUTTON_PIN,
            GPIO.FALLING,
            callback=self._left_button_callback,
            bouncetime=200,
        )
        GPIO.add_event_detect(
            Config.RIGHT_BUTTON_PIN,
            GPIO.FALLING,
            callback=self._right_button_callback,
            bouncetime=200,
        )
        while not self.stop_event.is_set():
            try:
                wait(
                    lambda: self.stop_event.is_set(), timeout_seconds=0.1  # pylint: disable=W0108
                )
            except TimeoutExpired:
                pass

        self.producer.close()

    def _left_button_callback(self, *args: Any) -> None:  # pylint: disable=W0613
        """Callback for left button"""
        if self.producer:
            time.sleep(0.01)
            self.producer.send(
                Config.KAFKA_VIEW_MANAGER_TOPIC, bytes("prev", encoding="utf-8")
            )

    def _right_button_callback(self, *args: Any) -> None:  # pylint: disable=W0613
        """Callback for right button"""
        if self.producer:
            time.sleep(0.01)
            self.producer.send(
                Config.KAFKA_VIEW_MANAGER_TOPIC, bytes("next", encoding="utf-8")
            )

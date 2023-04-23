"""
View class tests
"""

import time
from unittest.mock import Mock

from src.producer import Producer

class TestProducer:
    def test_init(self, mocker):
        producer = Producer()
        assert producer.order == 'next'

        mocker.patch("config.Config.PRODUCER_ASC_ORDER", False)
        producer = Producer()
        assert producer.order == 'prev'

    def test_stop(self, mocker):
        producer = Producer()
        producer.stop_event = Mock()
        producer.stop_event.set = Mock()

        producer.stop()
        producer.stop_event.set.assert_called_once()

    def test_run(self, mocker):
        mocker.patch("config.Config.PRODUCER_INTERVAL", 1)

        mocked_kafka_producer = Mock()
        mocked_kafka_producer.send = Mock()
        mocked_kafka_producer.close = Mock()
        mock = Mock(return_value=mocked_kafka_producer)

        mocker.patch('src.producer.KafkaProducer', mock)
        producer = Producer()

        producer.start()
        time.sleep(3)
        producer.stop()
        producer.join()

        assert mock.call_count == 1
        assert mocked_kafka_producer.send.call_count == 2
        assert mocked_kafka_producer.close.call_count == 1
        mocked_kafka_producer.send.assert_called_with('epd_rpi_view_manager_tests', b'next')

    def test_run_desc_order(self, mocker):
        mocker.patch("config.Config.PRODUCER_INTERVAL", 1)
        mocker.patch("config.Config.PRODUCER_ASC_ORDER", False)

        mocked_kafka_producer = Mock()
        mocked_kafka_producer.send = Mock()
        mocked_kafka_producer.close = Mock()
        mock = Mock(return_value=mocked_kafka_producer)

        mocker.patch('src.producer.KafkaProducer', mock)
        producer = Producer()

        producer.start()
        time.sleep(3)
        producer.stop()
        producer.join()

        assert mock.call_count == 1
        assert mocked_kafka_producer.send.call_count == 2
        assert mocked_kafka_producer.close.call_count == 1
        mocked_kafka_producer.send.assert_called_with('epd_rpi_view_manager_tests', b'prev')

    def test_run_send_called_once(self, mocker):
        mocker.patch("config.Config.PRODUCER_INTERVAL", 2)

        mocked_kafka_producer = Mock()
        mocked_kafka_producer.send = Mock()
        mocked_kafka_producer.close = Mock()
        mock = Mock(return_value=mocked_kafka_producer)

        mocker.patch('src.producer.KafkaProducer', mock)
        producer = Producer()

        producer.start()
        time.sleep(3)
        producer.stop()
        producer.join()

        assert mock.call_count == 1
        mocked_kafka_producer.send.assert_called_once_with('epd_rpi_view_manager_tests', b'next') 
        assert mocked_kafka_producer.close.call_count == 1
            
    def test_run_stopped_before_sending(self, mocker):
        mocker.patch("config.Config.PRODUCER_INTERVAL", 3)

        mocked_kafka_producer = Mock()
        mocked_kafka_producer.send = Mock()
        mocked_kafka_producer.close = Mock()
        mock = Mock(return_value=mocked_kafka_producer)

        mocker.patch('src.producer.KafkaProducer', mock)
        producer = Producer()

        producer.start()
        time.sleep(1)
        producer.stop()
        producer.join()

        assert mock.call_count == 1
        assert not mocked_kafka_producer.send.called
        assert mocked_kafka_producer.close.call_count == 1

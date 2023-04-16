"""
Consumer class tests
"""

import time
from unittest.mock import Mock, MagicMock

import src.consumer
from src.consumer import Consumer

class TestConsumer:
    def test_stop(self, mocker):
        mocked_view_manager = Mock()
        consumer = Consumer(mocked_view_manager)
        consumer.stop_event = Mock()
        consumer.stop_event.set = Mock()

        consumer.stop()
        consumer.stop_event.set.assert_called_once()

    def test_run(self, mocker):
        mocked_view_manager = Mock()
        mocked_kafka_consumer = MagicMock()
        mocked_kafka_consumer.__iter__.return_value = []
        mocked_kafka_consumer.close = Mock()
        mocked_kafka_consumer.subscribe = Mock()
        mock = Mock(return_value=mocked_kafka_consumer)

        mocker.patch('src.consumer.KafkaConsumer', mock)
        
        consumer = Consumer(mocked_view_manager)
        
        consumer.start()
        time.sleep(0.5)
        consumer.stop()
        consumer.join()

        assert mocked_kafka_consumer.subscribe.called
        assert mocked_kafka_consumer.close.called

    def test_run_prev_message(self, mocker):
        mocked_view_manager = Mock()
        mocked_message = Mock()
        mocked_message.value = bytes('prev', encoding='utf-8')
        mocked_kafka_consumer = MagicMock()
        mocked_kafka_consumer.__iter__.return_value = [mocked_message]
        mocked_kafka_consumer.close = Mock()
        mocked_kafka_consumer.subscribe = Mock()
        mock = Mock(return_value=mocked_kafka_consumer)

        mocker.patch('src.consumer.KafkaConsumer', mock)
        
        consumer = Consumer(mocked_view_manager)
        consumer.prev = Mock()
        consumer.next = Mock()

        consumer.start()
        time.sleep(0.5)
        consumer.stop()
        consumer.join()

        assert mocked_kafka_consumer.subscribe.called
        assert consumer.prev.called
        assert not consumer.next.called
        assert mocked_kafka_consumer.close.called

    def test_run_next_message(self, mocker):
        mocked_view_manager = Mock()
        mocked_message = Mock()
        mocked_message.value = bytes('next', encoding='utf-8')
        mocked_kafka_consumer = MagicMock()
        mocked_kafka_consumer.__iter__.return_value = [mocked_message]
        mocked_kafka_consumer.close = Mock()
        mocked_kafka_consumer.subscribe = Mock()
        mock = Mock(return_value=mocked_kafka_consumer)

        mocker.patch('src.consumer.KafkaConsumer', mock)
        
        consumer = Consumer(mocked_view_manager)
        consumer.prev = Mock()
        consumer.next = Mock()

        consumer.start()
        time.sleep(0.5)
        consumer.stop()
        consumer.join()

        assert mocked_kafka_consumer.subscribe.called
        assert not consumer.prev.called
        assert consumer.next.called
        assert mocked_kafka_consumer.close.called

    def test_run_stop_message(self, mocker):
        mocked_view_manager = Mock()
        mocked_message = Mock()
        mocked_message.value = bytes('stop', encoding='utf-8')
        mocked_kafka_consumer = MagicMock()
        mocked_kafka_consumer.__iter__.return_value = [mocked_message]
        mocked_kafka_consumer.close = Mock()
        mocked_kafka_consumer.subscribe = Mock()
        mock = Mock(return_value=mocked_kafka_consumer)

        mocker.patch('src.consumer.KafkaConsumer', mock)
        
        consumer = Consumer(mocked_view_manager)
        consumer.prev = Mock()
        consumer.next = Mock()

        consumer.start()
        time.sleep(0.5)
        consumer.join()

        assert mocked_kafka_consumer.subscribe.called
        assert not consumer.prev.called
        assert not consumer.next.called
        assert mocked_kafka_consumer.close.called

    def test_run_invalid_message(self, mocker):
        mocked_view_manager = Mock()
        mocked_message = Mock()
        mocked_message.value = 'invalid_message'
        mocked_kafka_consumer = MagicMock()
        mocked_kafka_consumer.__iter__.return_value = [mocked_message]
        mocked_kafka_consumer.close = Mock()
        mocked_kafka_consumer.subscribe = Mock()
        mock = Mock(return_value=mocked_kafka_consumer)

        mocker.patch('src.consumer.KafkaConsumer', mock)
        
        consumer = Consumer(mocked_view_manager)
        consumer.prev = Mock()
        consumer.next = Mock()

        consumer.start()
        time.sleep(0.5)
        consumer.stop()
        consumer.join()

        assert mocked_kafka_consumer.subscribe.called
        assert not consumer.prev.called
        assert not consumer.next.called
        assert mocked_kafka_consumer.close.called

    def test_prev(self, mocker):
        mocked_view_manager = Mock()
        mocked_view_manager.prev = Mock()

        consumer = Consumer(mocked_view_manager)
        consumer.prev()

        assert mocked_view_manager.prev.called

    def test_next(self, mocker):
        mocked_view_manager = Mock()
        mocked_view_manager.next = Mock()

        consumer = Consumer(mocked_view_manager)
        consumer.next()

        assert mocked_view_manager.next.called

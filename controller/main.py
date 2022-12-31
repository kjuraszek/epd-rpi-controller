import time
import logging
import importlib
from copy import deepcopy

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import UnknownTopicOrPartitionError, TopicAlreadyExistsError, NoBrokersAvailable, NodeNotReadyError

from config import KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL, EPD_MODEL, MOCKED_EPD_WIDTH, MOCKED_EPD_HEIGHT, CLEAR_EPD_ON_EXIT, USE_BUTTONS, KAFKA_BOOTSTRAP_SERVER
from src import Consumer, Producer, ViewManager
from src.api import MainAPI
from src.helpers import validate_config, validate_views
from custom_views import VIEWS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    validate_config()
    validate_views()

    if EPD_MODEL == 'mock':
        from src import MockedEPD
        epd = MockedEPD(width = MOCKED_EPD_WIDTH, height = MOCKED_EPD_HEIGHT)
    else:
        epd = importlib.import_module(f'waveshare_epd_driver.{EPD_MODEL}.EPD')

    if USE_BUTTONS:
        from src import ButtonManager

    for number in range(1, 8):
        try:
            kafka_admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER, api_version=(2, 5, 0))
            break
        except (NoBrokersAvailable, NodeNotReadyError) as e:
            if number == 5:
                raise e
            logger.error(f'Failed to connect with Kafka broker, retrying in: {number * 10} seconds.')
            time.sleep(number * 10)

    topic = NewTopic(name=KAFKA_VIEW_MANAGER_TOPIC,
                     num_partitions=1,
                     replication_factor=1,
                     topic_configs={'retention.ms':'60000'})
    try:
        kafka_admin.delete_topics([KAFKA_VIEW_MANAGER_TOPIC])
        time.sleep(2)
        logger.debug('topic deleted')
    except UnknownTopicOrPartitionError:
        logger.debug('unable to delete topic')
    kafka_admin.create_topics([topic])


    views = deepcopy(VIEWS)
    for view in views:
        view.epd = epd

    view_manager = ViewManager(views, epd)
    consumer = Consumer(view_manager)
    producer = Producer(asc_order=True)
    api = MainAPI(view_manager)

    tasks = [
        consumer,
        view_manager,
        api
    ]
    
    if PRODUCER_INTERVAL > 0: tasks.append(producer)

    if USE_BUTTONS: tasks.append(ButtonManager())

    for task in tasks:
        task.start()

    while not tasks[0].stop_event.is_set():
        time.sleep(1)

    try:
        kafka_admin.delete_topics([KAFKA_VIEW_MANAGER_TOPIC])
        logger.debug('topic deleted')
    except TopicAlreadyExistsError:
        logger.debug('unable to delete topic')

    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()

    if CLEAR_EPD_ON_EXIT:
        epd.Clear(0xFF)


if __name__ == '__main__':
    main()

import time
import logging
from copy import deepcopy

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import UnknownTopicOrPartitionError, TopicAlreadyExistsError

from config import KAFKA_VIEW_MANAGER_TOPIC, PRODUCER_INTERVAL, USE_MOCKED_EPD, MOCKED_EPD_WIDTH, MOCKED_EPD_HEIGHT
from src import Consumer, Producer, ViewManager
from src.helpers import validate_config, validate_views
from custom_views import VIEWS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    validate_config()
    validate_views()

    if USE_MOCKED_EPD:
        from src import MockedEPD
        epd = MockedEPD(width = MOCKED_EPD_WIDTH, height = MOCKED_EPD_HEIGHT)
    else:
        raise NotImplementedError

    kafka_admin = KafkaAdminClient(bootstrap_servers='localhost:9092')

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

    tasks = [
        consumer,
        view_manager
    ]
    
    if PRODUCER_INTERVAL > 0: tasks.append(producer)

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


if __name__ == '__main__':
    main()

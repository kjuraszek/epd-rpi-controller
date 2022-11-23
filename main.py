import threading
import time
import logging

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import UnknownTopicOrPartitionError, TopicAlreadyExistsError

from waiting import wait, TimeoutExpired

from config import cfg

KAFKA_VIEW_MANAGER_TOPIC  = cfg['kafka'].get('view_manager_topic', 'epd_rpi_view_manager')
PRODUCER_INTERVAL = cfg['main'].getint('producer_interval', 0)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class View:
    '''
    view
    '''
    def __init__(self, epd, name, interval):
        self.epd = epd
        self.name = name
        self.interval = interval

    def show(self):
        raise NotImplementedError


class DummyView(View):
    '''
    dummy view
    '''
    def show(self):
        logger.info('%s is running', self.name)
        time.sleep(2)


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
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
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
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe([KAFKA_VIEW_MANAGER_TOPIC])

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
                except:
                    logger.error('Consumer decoding error with %s', message.value)
                if self.stop_event.is_set():
                    logger.info('Stopping consumer')
                    break

        consumer.close()

    def prev(self):
        self.view_manager.prev()
    
    def next(self):
        self.view_manager.next()
        

class ViewManager(threading.Thread):
    '''
    view manager
    '''
    def __init__(self, views, starting_view = 0):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.busy = threading.Event()
        self.current_view = starting_view
        self.views = views
        self.action = None
    
    def next(self):
        if not self.busy.is_set():
            self.busy.set()
            self.action = 'next'
        else:
            logger.debug('View manager is busy')

    def prev(self):
        if not self.busy.is_set():
            self.busy.set()
            self.action = 'prev'
        else:
            logger.debug('View manager is busy')
        
    def stop(self):
        self.stop_event.set()
    
    def run(self):
        switched = False
        while not self.stop_event.is_set():
            if self.busy.is_set() and self.action in ('next', 'prev'):
                if self.action == 'next':
                    self.current_view = self.current_view + 1 if self.current_view < len(self.views) - 1 else 0
                else:
                    self.current_view = self.current_view - 1 if self.current_view > 0 else len(self.views) - 1
                switched = False
            if not switched:
                self.busy.set()
                logger.debug('\tView is running')
                self.views[self.current_view].show()
                logger.debug('\tView is idle')
                self.busy.clear()
                if self.views[self.current_view].interval == 0:
                    switched = True
                else:
                    switched = False
                    try:
                        wait(lambda : self.busy.is_set() or self.stop_event.is_set(),
                             timeout_seconds=self.views[self.current_view].interval)
                    except TimeoutExpired:
                        continue
                    else:
                        if self.stop_event.is_set():
                            break
                        if self.busy.is_set():
                            continue


def main():
    
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
    
    epd = None
    
    views = [
        DummyView(epd, 'Dummy view 1', 0),
        DummyView(epd, 'Dummy view 2', 6),
        DummyView(epd, 'Dummy view 3', 0),
        DummyView(epd, 'Dummy view 4', 7)
    ]

    view_manager = ViewManager(views)
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

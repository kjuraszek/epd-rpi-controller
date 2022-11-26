import configparser

cfg = configparser.ConfigParser()
cfg.read('epd-rpi-controller.cfg')

KAFKA_VIEW_MANAGER_TOPIC  = cfg['kafka'].get('view_manager_topic')
PRODUCER_INTERVAL = cfg['main'].getint('producer_interval')

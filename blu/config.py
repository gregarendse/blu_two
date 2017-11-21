import logging

import yaml

logger = logging.getLogger(__name__)


class Config(object):
    __instance__ = None
    cfg = {}

    def __new__(cls, *args, **kwargs):
        if Config.__instance__ is None:
            Config.__instance__ = object.__new__(cls)
        return Config.__instance__

    def load(self, location: str = "blu.yml"):
        logger.info('loading configuration, source: %s', location)
        with open(location, 'r') as file:
            self.cfg = yaml.load(file)

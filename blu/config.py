import yaml


class Config(object):
    __instance__ = None
    cfg = {}

    def __new__(cls, *args, **kwargs):
        if Config.__instance__ is None:
            Config.__instance__ = object.__new__(cls)
        return Config.__instance__

    def load(self, location: str = "blu.yml"):
        with open(location, 'r') as file:
            self.cfg = yaml.load(file)

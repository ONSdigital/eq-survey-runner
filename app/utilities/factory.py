class Factory(object):

    def __init__(self):
        self._map = {}

    def register(self, key, cls):
        self._map[key] = cls

    def register_all(self, map):
        self._map = map

    def create(self, key, *args):
        if key in self._map:
            cls = self._map[key]
            return cls(*args)
        else:
            raise ValueError("Key {key} not registered with factory".format(key=key))


factory = Factory()

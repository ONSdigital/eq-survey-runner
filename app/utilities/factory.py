class Factory(object):

    def __init__(self):
        self._map = {}

    def register(self, key, cls):
        self._map[key] = cls

    def register_all(self, _map):
        self._map = _map

    def create(self, key, *args):
        if key in self._map:
            cls = self._map[key]
            return cls(*args)
        else:
            raise ValueError("Key {key} not registered with factory".format(key=key))


factory = Factory()

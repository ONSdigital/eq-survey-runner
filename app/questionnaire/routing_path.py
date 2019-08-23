class RoutingPath:
    """Holds a list of locations and optimizes for `in` comparisons
    """

    def __init__(self, path):
        self._values = tuple(path)
        self._set = frozenset(path)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, key):
        return self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __reversed__(self):
        return reversed(self._values)

    def __contains__(self, key):
        return key in self._set

    def __eq__(self, other):
        other_values = other
        if isinstance(other, RoutingPath):
            other_values = other._values  # pylint: disable=protected-access

        elif isinstance(other, list):
            other_values = tuple(other)

        return self._values == other_values

    def index(self, *args):
        return self._values.index(*args)


class FlushPermissionDenied(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value

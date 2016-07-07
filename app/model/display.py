from app.model.properties import Properties


class Display(object):

    def __init__(self, properties=None):
        self.properties = Properties()
        if properties is not None:
            self.properties = properties

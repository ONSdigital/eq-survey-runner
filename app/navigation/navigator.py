class Navigator(object):
    # destination  "group:block:section:question:<repetition>"
    def _valid_destination(self, destination):
        raise NotImplementedError()

    def get_current_location(self):
        raise NotImplementedError()

    def go_to(self, location):
        raise NotImplementedError()

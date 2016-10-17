
class UserJourney(object):
    def __init__(self, current_node, first_node, tail_node, archive, submitted_at, valid_locations):
        self.current = current_node
        self.first = first_node
        self.tail = tail_node
        self.archive = archive
        self.submitted_at = submitted_at
        self.valid_locations = valid_locations

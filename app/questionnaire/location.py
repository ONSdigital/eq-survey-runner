class Location(object):

    def __init__(self, group_id, group_instance, block_id):

        self.group_id = group_id
        self.group_instance = group_instance
        self.block_id = block_id

    def __eq__(self, other):
        return self.group_id == other.group_id and \
               self.group_instance == other.group_instance and \
               self.block_id == other.block_id

    def __str__(self):
        return "{}/{}/{}".format(self.group_id, self.group_instance, self.block_id)

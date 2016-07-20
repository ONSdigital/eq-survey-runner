class RoutingException(Exception):
    pass


class RoutingEngine(object):
    ''' The routing engine will apply any routing rules dependant on where the user is in the schema
    and what answers they have provided.
    '''
    def __init__(self, schema_model):
        self._schema = schema_model

    def get_next_location(self, current_location):
        if current_location == 'introduction':
            next_location = self._schema.groups[0].blocks[0].id
        elif current_location == 'summary':
            next_location = 'thank-you'
        else:
            current_block = self._schema.get_item_by_id(current_location)
            if current_block:
                current_group = current_block.container

                for index, block in enumerate(current_group.blocks):
                    if block.id == current_block.id:
                        if index + 1 < len(current_group.blocks):
                            # return the next block in this group
                            return current_group.blocks[index + 1].id
                for index, group in enumerate(self._schema.groups):
                    if group.id == current_group.id:
                        if index + 1 < len(self._schema.groups):
                            # return the first block in the next group
                            return self._schema.groups[index + 1].blocks[0].id

                # There are no more blocks or groups, go to summary
                next_location = 'summary'
            else:
                raise RoutingException('Cannot route: No current block')
        return next_location

    def get_first_block(self):
        return self._schema.groups[0].blocks[0].id

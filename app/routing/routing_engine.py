from app.navigation.navigator import NavigationException


class RoutingEngine(object):
    def __init__(self, schema_model, response_store):
        self._schema = schema_model
        self._response_store = response_store

        # building routing rules

    def get_next(self, current_location, user_action):
        if user_action == 'start_questionnaire':
            # Get the first block id
            current_location = self._schema.groups[0].blocks[0].id

        elif user_action == 'save_continue':
            # We have already been validated so we only
            # need to figure out where to go next

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
                return 'summary'

            else:
                raise NavigationException('Cannot route: No current block')
        else:
            pass

        return current_location

import logging

from copy import deepcopy

from app.schema.answer import Answer


logger = logging.getLogger(__name__)


class RepeatingElementException(Exception):
    pass


class RepeatingElement(object):
    ''' The repeating element manager will create a new element with new ids and q-codes using the
        repetition number as an identifier (e.g. item.id_repetition number)
    '''

    def __init__(self, questionnaire_manager):
        self._questionnaire_manager = questionnaire_manager

    def create_element(self, current_element):

        next_repetition = current_element.repetition + 1
        new_element_id = self._rename_id(current_element.id, next_repetition)

        # Check to see if we can create the element
        if not self._questionnaire_manager.check_item_exists_in_schema(new_element_id):
            new_element = self._clone_element(current_element, new_element_id, next_repetition)
            self._update_state(new_element)
        else:
            # re-attach it, if it is in the archive
            self._questionnaire_manager.go_to_state(new_element_id)

        return new_element_id

    def _clone_element(self, current_element, new_element_id, next_repetition):
        # Copy the current element and update its ids

        new_element = deepcopy(current_element)
        new_element.repetition = next_repetition
        new_element.id = new_element_id
        self._update_ids_and_q_codes(new_element, next_repetition)
        return new_element

    def _update_ids_and_q_codes(self, item, next_repetition):
        # Recursive function updating all item ids and q_codes to include the repetition number

        if isinstance(item, Answer):
            item.widget.name = self._rename_id(item.widget.name, next_repetition)
            item.code = self._rename_id(item.code, next_repetition)
        else:
            for child in item.children:
                child.id = self._rename_id(child.id, next_repetition)
                logging.debug("registering item %s", child)
                self._questionnaire_manager.register_element_in_schema(child)
                # Repeat the above function with any children
                self._update_ids_and_q_codes(child, next_repetition)

    @staticmethod
    def _rename_id(current_id, repetition):
        logging.debug("Updating id for %s, repetition %s", current_id, repetition)
        # Take of any previous repetition numbers
        return current_id.rsplit('_', 1)[0] + "_" + str(repetition)

    def _update_state(self, new_element):
        logging.debug("Registering new element %s in schema and updating state", new_element.id)
        self._questionnaire_manager.add_repeating_element(new_element)

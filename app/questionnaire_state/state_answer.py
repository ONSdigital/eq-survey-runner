from app.data_model.answer_store import Answer
from app.questionnaire_state.state_item import StateItem


class StateAnswer(StateItem):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)
        # typed value
        self.value = None
        # actual user input
        self.input = None
        self.other = None

    def update_state(self, user_input):

        # Clear any previous value and validation results
        self.value = None
        self.is_valid = True
        self.errors = []
        # Get the user input
        # Todo, there shouldn't be a need for both self.input and self.value, but self.value gets changed later in the code
        self.input = self.schema_item.get_user_input(user_input)
        self.value = self.schema_item.get_user_input(user_input)
        self.other = self.schema_item.get_other_value(user_input)
        if self.schema_item.type == 'Radio' and self.input:
            self._restore_other_value(user_input)

    def _restore_other_value(self, user_input):
        # Get radio options from the schema.
        for option in self.schema_item.options:
            # If the radio answer has an Other option...
            is_other_radio_option = option['label'] == 'Other' and 'other' in option

            if is_other_radio_option:
                schema_options = [option['value'] for option in self.schema_item.options]

                if self.input not in schema_options:
                    # Input is not a pre-defined answer so it must be the user-entered value for other
                    self.input = 'other'
                    self.value = 'other'
                    self.other = self.schema_item.get_user_input(user_input)

    def get_answers(self):
        return [self]

    def flatten(self):
        return Answer(
            block_id=self.parent.parent.parent.id,
            answer_id=self.id,
            answer_instance=self.answer_instance,
            group_id=self.schema_item.container.container.container.container.id,
            group_instance=self.group_instance,
            value=self.value,
        )

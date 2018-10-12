from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules import evaluate_skip_conditions, evaluate_repeat


class Completeness:
    NOT_STARTED = 'NOT_STARTED'
    STARTED = 'STARTED'
    SKIPPED = 'SKIPPED'
    COMPLETED = 'COMPLETED'
    INVALID = 'INVALID'

    # for the purposes of deriving completeness all of the following states
    # allow a block to be marked as complete so long as at least
    # one item is complete
    COMPLETED_STATES = (COMPLETED, INVALID, SKIPPED)

    def __init__(self, schema, answer_store, completed_blocks, routing_path, metadata):
        self.answer_store = answer_store
        self.completed_blocks = completed_blocks
        self.routing_path = routing_path
        self.metadata = metadata
        self.schema = schema

    def is_section_complete(self, section):
        return self.get_state_for_section(section) == self.COMPLETED

    def is_group_complete(self, group, group_instance=None):
        return self.get_state_for_group(group, group_instance=group_instance) == self.COMPLETED

    def is_block_complete(self, location):
        return location in self.completed_blocks

    def all_sections_complete(self):
        return all(state in self.COMPLETED_STATES for state in self._get_all_section_states())

    def any_section_complete(self):
        return any(state == self.COMPLETED for state in self._get_all_section_states())

    def get_state_for_section(self, section):
        if isinstance(section, str):
            # lookup section by section ID
            section = self.schema.get_section(section)

        group_states = [
            self.get_state_for_group(group) for group in section['groups']
        ]

        def eval_state(state_to_compare):
            return (state == state_to_compare for state in group_states)

        section_state = self.NOT_STARTED

        if group_states:
            if all(eval_state(self.SKIPPED)):
                section_state = self.SKIPPED

            elif all(eval_state(self.INVALID)):
                section_state = self.INVALID

            elif any(eval_state(self.STARTED)):
                section_state = self.STARTED

            elif all(state in self.COMPLETED_STATES for state in group_states):
                section_state = self.COMPLETED

        return section_state

    def get_state_for_group(self, group, group_instance=0, group_instance_id=None):
        if isinstance(group, str):
            # lookup group by group ID
            group = self.schema.get_group(group)

        if (QuestionnaireSchema.is_confirmation_group(group) or
                QuestionnaireSchema.is_summary_group(group)):
            # summary/confirmations are special cases as we don't want to
            # render until the whole survey is complete. They're also never
            # show as complete
            return self.NOT_STARTED if self.all_sections_complete() else self.SKIPPED

        if self._should_skip(group, group_instance, group_instance_id):
            return self.SKIPPED

        block_states = [
            state for location, state in
            self._get_block_states_for_group(group, group_instance)
        ]

        def eval_state(state_to_compare):
            return (state == state_to_compare for state in block_states)

        group_state = self.NOT_STARTED

        if all(eval_state(self.SKIPPED)):
            group_state = self.SKIPPED

        elif not self.routing_path:
            group_state = self.NOT_STARTED

        elif all(eval_state(self.INVALID)):
            group_state = self.INVALID

        elif all(state in self.COMPLETED_STATES for state in block_states):
            group_state = self.COMPLETED

        elif any(eval_state(self.COMPLETED)):
            group_state = self.STARTED

        return group_state

    def get_first_incomplete_location_in_survey(self):
        incomplete_locations = (
            self.get_first_incomplete_location_in_section(section)
            for section in self.schema.sections
        )
        return next(filter(None, incomplete_locations), None)

    def get_first_incomplete_location_in_section(self, section):
        incomplete_locations = (
            self.get_first_incomplete_location_in_group(group)
            for group in section['groups']
        )
        return next(filter(None, incomplete_locations), None)

    def get_first_incomplete_location_in_group(self, group, group_instance=0):
        if self._should_skip(group, group_instance):
            return

        incomplete_locations = (
            location for location, state in
            self._get_block_states_for_group(
                group, group_instance=group_instance)
            if state not in self.COMPLETED_STATES
        )
        return next(incomplete_locations, None)

    def _get_block_states_for_group(self, group, group_instance=0):
        repeating_rule = self.schema.get_repeat_rule(group)

        if repeating_rule:
            max_instance = evaluate_repeat(repeating_rule, self.answer_store, self.schema, self.routing_path) - 1
            start_instance = 0
        else:
            start_instance = max_instance = group_instance

        for current_instance in range(start_instance, max_instance + 1):
            for block in group['blocks']:
                location = Location(group['id'], current_instance, block['id'])

                if self._should_skip(block, group_instance):
                    state = self.SKIPPED
                elif self._is_valid_for_completeness(block, location):
                    state = self.COMPLETED if self.is_block_complete(location) else self.NOT_STARTED
                else:
                    # block is not a question block or is not on the routing path
                    state = self.INVALID

                yield location, state

    def _get_all_section_states(self):
        return (
            self.get_state_for_section(section)
            for section in self._get_all_question_sections()
        )

    def _get_all_question_sections(self):
        return (
            section for section in self.schema.sections
            if not (
                QuestionnaireSchema.is_summary_section(section) or
                QuestionnaireSchema.is_confirmation_section(section))
        )

    def _should_skip(self, group_or_block, group_instance, group_instance_id=None):
        return (
            'skip_conditions' in group_or_block and
            evaluate_skip_conditions(group_or_block['skip_conditions'], self.schema, self.metadata, self.answer_store, group_instance, group_instance_id)
        )

    def _is_valid_for_completeness(self, block, location):
        """Returns True if the given block should be checked for completeness
        """
        return block['type'] in ('Question', 'ConfirmationQuestion') and location in self.routing_path

from app.data_model.answer_store import Answer
from app.questionnaire.location import Location


class AnswerStoreUpdater:
    """Component responsible for any actions that need to happen as a result of updating the answer store
    """
    def __init__(self, current_location, schema, questionnaire_store):
        self._current_location = current_location
        self._schema = schema
        self._questionnaire_store = questionnaire_store

    def save_form(self, form):
        if self._should_save_serialised_answers():
            self._update_questionnaire_store_with_answer_data(form.serialise())
        else:
            self._update_questionnaire_store_with_form_data(form.data)

        self._questionnaire_store.add_or_update()

    def _update_questionnaire_store_with_answer_data(self, data):
        survey_answer_ids = self._schema.get_answer_ids_for_block(self._current_location.block_id)

        valid_answers = (
            answer for answer in data
            if answer.answer_id in survey_answer_ids
        )
        for answer in valid_answers:
            self._questionnaire_store.answer_store.add_or_update(answer)

        if self._current_location not in self._questionnaire_store.completed_blocks:
            self._questionnaire_store.completed_blocks.append(self._current_location)

    def _update_questionnaire_store_with_form_data(self, data):
        survey_answer_ids = self._schema.get_answer_ids_for_block(self._current_location.block_id)

        for answer_id, answer_value in data.items():

            # If answer is not answered then check for a schema specified default
            if answer_value is None:
                answer_value = self._schema.get_answer(answer_id).get('default')

            if answer_id in survey_answer_ids:
                if answer_value is not None:
                    answer = Answer(answer_id=answer_id,
                                    value=answer_value,
                                    group_instance=self._current_location.group_instance)

                    latest_answer_store_hash = self._questionnaire_store.answer_store.get_hash()
                    self._questionnaire_store.answer_store.add_or_update(answer)
                    if (latest_answer_store_hash != self._questionnaire_store.answer_store.get_hash() and
                            self._schema.dependencies[answer_id]):
                        self._remove_dependent_answers_from_completed_blocks(answer_id, self._current_location.group_instance)
                else:
                    self._remove_answer_from_questionnaire_store(
                        answer_id,
                        group_instance=self._current_location.group_instance)

        if self._current_location not in self._questionnaire_store.completed_blocks:
            self._questionnaire_store.completed_blocks.append(self._current_location)

    def _remove_dependent_answers_from_completed_blocks(self, answer_id, group_instance):
        """
        Gets a list of answers ids that are dependent on the answer_id passed in.
        Then for each dependent answer it will remove it's block from those completed.
        This will therefore force the respondent to revisit that block.
        The dependent answers themselves remain untouched.
        :param answer_id: the answer that has changed
        :return: None
        """
        answer_in_repeating_group = self._schema.answer_is_in_repeating_group(answer_id)
        dependencies = self._schema.dependencies[answer_id]

        for dependency in dependencies:
            dependency_in_repeating_group = self._schema.answer_is_in_repeating_group(dependency)

            answer = self._schema.get_answer(dependency)
            question = self._schema.get_question(answer['parent_id'])
            block = self._schema.get_block(question['parent_id'])

            if dependency_in_repeating_group and not answer_in_repeating_group:
                self._questionnaire_store.remove_completed_blocks(group_id=block['parent_id'], block_id=block['id'])
            else:
                location = Location(block['parent_id'], group_instance, block['id'])
                self._questionnaire_store.remove_completed_blocks(location=location)

    def _remove_answer_from_questionnaire_store(self, answer_id, group_instance=0):
        self._questionnaire_store.answer_store.remove(answer_ids=[answer_id],
                                                      group_instance=group_instance,
                                                      answer_instance=0)

    def _should_save_serialised_answers(self):
        """Returns `True` if the answer store should be updated with answer values provided by a form's
        serialise() method rather than those processed by the form object
        """
        return self._current_location.block_id in ['relationships', 'household-relationships', 'household-composition']

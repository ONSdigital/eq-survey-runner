from typing import List, Tuple
from app.data_model.answer_store import Answer


class QuestionnaireStoreUpdater:
    """ Component responsible for any actions that need to happen as a result of updating the questionnaire_store
    """

    EMPTY_ANSWER_VALUES: Tuple = (None, [], '')

    def __init__(self, current_location, schema, questionnaire_store, current_question):
        self._current_location = current_location
        self._current_question = current_question or {}
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._answer_store = self._questionnaire_store.answer_store
        self._list_store = self._questionnaire_store.list_store

    def save_answers(self, form, save_completed_blocks=True):
        self._update_questionnaire_store_with_form_data(form.data)

        if save_completed_blocks:
            if self._current_location not in self._questionnaire_store.completed_blocks:
                self._questionnaire_store.completed_blocks.append(
                    self._current_location
                )

        self._questionnaire_store.add_or_update()

    def save_new_list_item_answers(self, form, list_name):
        new_list_item_id = self._list_store.add_list_item(list_name)

        self._current_location.list_item_id = new_list_item_id

        self.save_answers(form, False)

    def _update_questionnaire_store_with_form_data(self, form_data):
        answer_ids_for_question = self._schema.get_answer_ids_for_question(
            self._current_question
        )

        for answer_id, answer_value in form_data.items():

            # If answer is not answered then check for a schema specified default
            if answer_value in self.EMPTY_ANSWER_VALUES:
                answer = next(
                    (
                        answer
                        for answer in self._current_question.get('answers', [])
                        if answer['id'] == answer_id
                    ),
                    {},
                )
                answer_value = answer.get('default')

            if answer_id in answer_ids_for_question:
                if answer_value not in self.EMPTY_ANSWER_VALUES:
                    answer = Answer(
                        answer_id=answer_id,
                        list_item_id=self._current_location.list_item_id,
                        value=answer_value,
                    )

                    self._answer_store.add_or_update(answer)
                else:
                    self._answer_store.remove_answer(answer_id)

    def remove_all_answers_with_list_item_id(self, list_name: str, list_item_id: str):
        """ Remove answers from the answer store and update the list store to remove it
        """
        self._list_store.delete_list_item_id(list_name, list_item_id)

        self._answer_store.remove_all_answers_for_list_item_id(
            list_item_id=list_item_id
        )

        self._questionnaire_store.add_or_update()

    def remove_answer_ids(self, answer_ids: List):
        for answer_id in answer_ids:
            self._answer_store.remove_answer(answer_id)
        self._questionnaire_store.add_or_update()

    def remove_completed_blocks(self, location):
        self._questionnaire_store.remove_completed_blocks(location)
        self._questionnaire_store.add_or_update()

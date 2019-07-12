from typing import List, Tuple

from app.data_model.answer_store import Answer
from app.data_model.relationship_store import Relationship, RelationshipStore


class QuestionnaireStoreUpdater:
    """ Component responsible for any actions that need to happen as a result of updating the questionnaire_store
    """

    EMPTY_ANSWER_VALUES: Tuple = (None, [], '')

    def __init__(self, current_location, schema, questionnaire_store, current_question):
        current_section_id = schema.get_section_for_block_id(current_location.block_id)[
            'id'
        ]
        self._current_location = current_location
        self._current_section_id = current_section_id
        self._current_question = current_question or {}
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._answer_store = self._questionnaire_store.answer_store
        self._list_store = self._questionnaire_store.list_store
        self._progress_store = self._questionnaire_store.progress_store

    def save(self):
        if self.is_dirty():
            self._questionnaire_store.save()

    def is_dirty(self):
        if (
            self._answer_store.is_dirty
            or self._list_store.is_dirty
            or self._progress_store.is_dirty
        ):
            return True
        return False

    def update_answers(self, form):
        self._update_questionnaire_store_with_form_data(form.data)

    def update_relationship_answer(self, form_data, from_list_item_id, to_list_item_id):
        relationship_answer_id = self._schema.get_relationship_answer_id_for_block(
            self._current_location.block_id
        )

        answer = self._answer_store.get_answer(relationship_answer_id)
        if answer:
            relationship_store = RelationshipStore(answer.value)
        else:
            relationship_store = RelationshipStore()

        relationship_answer = form_data.get(relationship_answer_id)

        relationship = Relationship(
            from_list_item_id, to_list_item_id, relationship_answer
        )
        relationship_store.add_or_update(relationship)

        self._answer_store.add_or_update(
            Answer(relationship_answer_id, relationship_store.serialise())
        )

    def remove_answers(self, answer_ids: List):
        for answer_id in answer_ids:
            self._answer_store.remove_answer(answer_id)

    def add_primary_person(self, list_name):
        if self._list_store[list_name].primary_person:
            return self._list_store[list_name].primary_person

        return self._list_store.add_list_item(list_name, primary_person=True)

    def add_list_item_and_answers(self, form, list_name):
        new_list_item_id = self._list_store.add_list_item(list_name)

        self._current_location.list_item_id = new_list_item_id

        self.update_answers(form)

    def remove_primary_person(self, list_name: str):
        """ Remove the primary person and all of their answers.
        Any context for the primary person will be removed
        """
        list_item_id = self._list_store[list_name].primary_person
        if list_item_id:
            self.remove_list_item_and_answers(list_name, list_item_id)

    def remove_list_item_and_answers(self, list_name: str, list_item_id: str):
        """ Remove answers from the answer store and update the list store to remove it
        """
        self._list_store.delete_list_item(list_name, list_item_id)

        self._answer_store.remove_all_answers_for_list_item_id(
            list_item_id=list_item_id
        )

    def add_completed_location(self, location=None, section_id=None):
        location = location or self._current_location
        section_id = section_id or self._current_section_id

        self._progress_store.add_completed_location(section_id, location)

    def remove_completed_location(self):
        self._progress_store.remove_completed_location(
            self._current_section_id, self._current_location
        )

    def update_section_status(self, section_status):
        self._progress_store.update_section_status(
            self._current_section_id, section_status
        )

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

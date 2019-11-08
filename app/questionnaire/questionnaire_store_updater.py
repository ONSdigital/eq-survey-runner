from itertools import combinations

from typing import List, Optional, Tuple, Union

from app.data_model.answer_store import Answer
from app.data_model.relationship_store import Relationship, RelationshipStore
from app.questionnaire.location import Location


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

    def update_relationship_answer(self, form_data, list_item_id, to_list_item_id):
        relationship_answer_id = self._schema.get_relationship_answer_id_for_block(
            self._current_location.block_id
        )
        answer = self._answer_store.get_answer(relationship_answer_id)
        self._create_relationship_store_and_update_answer(
            relationship_answer_id, answer, form_data, list_item_id, to_list_item_id
        )

    def _create_relationship_store_and_update_answer(
        self, relationship_answer_id, answer, form_data, list_item_id, to_list_item_id
    ):
        try:
            relationship_store = RelationshipStore(answer.value)
        except AttributeError:
            relationship_store = RelationshipStore()

        relationship_answer = form_data.get(relationship_answer_id)
        relationship = Relationship(list_item_id, to_list_item_id, relationship_answer)
        relationship_store.add_or_update(relationship)
        self._answer_store.add_or_update(
            Answer(relationship_answer_id, relationship_store.serialise())
        )

    def remove_completed_relationship_locations_for_list_name(
        self, list_name: str
    ) -> None:
        target_relationship_collectors = self._get_relationship_collectors_by_list_name(
            list_name
        )
        if target_relationship_collectors:
            for target in target_relationship_collectors:
                block_id = target['id']
                section_id = self._schema.get_section_for_block_id(block_id)['id']
                self.remove_completed_location(Location(section_id, block_id))

    def update_relationship_question_completeness(self, list_name: str) -> None:
        relationship_collectors = self._get_relationship_collectors_by_list_name(
            list_name
        )

        if not relationship_collectors:
            return None

        list_items = self._list_store.get(list_name).items

        for collector in relationship_collectors:

            relationship_answer_id = self._schema.get_relationship_answer_id_for_block(
                collector['id']
            )
            relationship_answers = self._get_relationships_in_answer_store(
                relationship_answer_id
            )

            if relationship_answers:
                pairs = {
                    (answer['list_item_id'], answer['to_list_item_id'])
                    for answer in relationship_answers
                }

                expected_pairs = set(combinations(list_items, 2))
                if expected_pairs == pairs:
                    section_id = self._schema.get_section_for_block_id(collector['id'])[
                        'id'
                    ]
                    location = Location(section_id, collector['id'])
                    self.add_completed_location(location)

    def _get_relationship_collectors_by_list_name(self, list_name: str):
        return self._schema.get_relationship_collectors_by_list_name(list_name)

    def _get_relationships_in_answer_store(self, relationship_answer_id: str):
        return self._answer_store.get_answer(relationship_answer_id).value

    def remove_answers(self, answer_ids: List):
        for answer_id in answer_ids:
            self._answer_store.remove_answer(answer_id)

    def add_primary_person(self, list_name):
        self.remove_completed_relationship_locations_for_list_name(list_name)

        if self._list_store[list_name].primary_person:
            return self._list_store[list_name].primary_person

        return self._list_store.add_list_item(list_name, primary_person=True)

    def add_list_item_and_answers(self, form, list_name):
        new_list_item_id = self._list_store.add_list_item(list_name)
        self._current_location.list_item_id = new_list_item_id
        self.update_answers(form)
        self.remove_completed_relationship_locations_for_list_name(list_name)

    def remove_primary_person(self, list_name: str):
        """ Remove the primary person and all of their answers.
        Any context for the primary person will be removed
        """
        list_item_id = self._list_store[list_name].primary_person
        if list_item_id:
            self.remove_list_item_and_answers(list_name, list_item_id)

    def remove_list_item_and_answers(self, list_name: str, list_item_id: str):
        """ Remove answers from the answer store and update the list store to remove it.
        Any related relationship answers are re-evaluated for completeness.
        """
        self._list_store.delete_list_item(list_name, list_item_id)

        self._answer_store.remove_all_answers_for_list_item_id(
            list_item_id=list_item_id
        )

        answers = self.get_relationship_answers_for_list_name(list_name)
        if answers:
            self.remove_relationship_answers_for_list_item_id(list_item_id, answers)
            self.update_relationship_question_completeness(list_name)

        self._progress_store.remove_progress_for_list_item_id(list_item_id=list_item_id)

    def get_relationship_answers_for_list_name(
        self, list_name: str
    ) -> Union[List[Answer], None]:
        assosciated_relationship_collectors = self._get_relationship_collectors_by_list_name(
            list_name
        )
        if not assosciated_relationship_collectors:
            return None

        relationship_answer_ids = [
            self._schema.get_relationship_answer_id_for_block(block['id'])
            for block in assosciated_relationship_collectors
        ]

        return self._answer_store.get_answers_by_answer_id(relationship_answer_ids)

    def remove_relationship_answers_for_list_item_id(
        self, list_item_id: str, answers: List
    ) -> None:
        for answer in answers:
            answers_to_keep = [
                value
                for value in answer.value
                if list_item_id not in {value['to_list_item_id'], value['list_item_id']}
            ]
            answer.value = answers_to_keep
            self._answer_store.add_or_update(answer)

    def add_completed_location(self, location: Optional[Location] = None):
        location = location or self._current_location

        self._progress_store.add_completed_location(location)

    def remove_completed_location(self, location: Optional[Location] = None):
        location = location or self._current_location
        self._progress_store.remove_completed_location(location)

    def update_section_status(
        self, section_status: str, section_id: str, list_item_id: Optional[str] = None
    ):
        self._progress_store.update_section_status(
            section_status, section_id, list_item_id
        )

    def _update_questionnaire_store_with_form_data(self, form_data):
        answer_ids_for_question = self._schema.get_answer_ids_for_question(
            self._current_question
        )

        for answer_id, answer_value in form_data.items():

            if answer_id in answer_ids_for_question:
                if answer_value not in self.EMPTY_ANSWER_VALUES:
                    answer = Answer(
                        answer_id=answer_id,
                        list_item_id=self._current_location.list_item_id,
                        value=answer_value,
                    )

                    self._answer_store.add_or_update(answer)
                else:
                    self._answer_store.remove_answer(
                        answer_id, self._current_location.list_item_id
                    )

from collections import defaultdict

from app.data_model.answer_store import Answer
from app.forms.questionnaire_form import QuestionnaireForm
from app.helpers.schema_helpers import get_group_instance_id
from app.questionnaire.location import Location


class AnswerStoreUpdater:
    """Component responsible for any actions that need to happen as a result of updating the answer store
    """

    def __init__(self, current_location, schema, questionnaire_store):
        self._current_location = current_location
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._answer_store = self._questionnaire_store.answer_store

    def save_answers(self, form):
        if isinstance(form, QuestionnaireForm):
            self._update_questionnaire_store_with_form_data(form.data)
        else:
            self._update_questionnaire_store_with_answer_data(form.serialise())

        if self._current_location not in self._questionnaire_store.completed_blocks:
            self._questionnaire_store.completed_blocks.append(self._current_location)

        self._questionnaire_store.add_or_update()

    def _update_questionnaire_store_with_answer_data(self, answers):
        survey_answer_ids = self._schema.get_answer_ids_for_block(self._current_location.block_id)

        valid_answers = (
            answer for answer in answers
            if answer.answer_id in survey_answer_ids
        )

        for answer in valid_answers:
            answer.group_instance_id = get_group_instance_id(self._schema, self._answer_store, self._current_location,
                                                             answer.answer_instance)
            self._answer_store.add_or_update(answer)

    def _update_questionnaire_store_with_form_data(self, answers):
        survey_answer_ids = self._schema.get_answer_ids_for_block(self._current_location.block_id)

        for answer_id, answer_value in answers.items():

            # If answer is not answered then check for a schema specified default
            if answer_value is None:
                answer_value = self._schema.get_answer(answer_id).get('default')

            if answer_id in survey_answer_ids:
                if answer_value is not None:
                    answer = Answer(answer_id=answer_id,
                                    value=answer_value,
                                    group_instance_id=get_group_instance_id(self._schema, self._answer_store,
                                                                            self._current_location),
                                    group_instance=self._current_location.group_instance)

                    latest_answer_store_hash = self._answer_store.get_hash()
                    self._answer_store.add_or_update(answer)

                    if latest_answer_store_hash != self._answer_store.get_hash() and self._schema.answer_dependencies[answer_id]:
                        self._remove_dependent_answers_from_completed_blocks(answer_id)
                else:
                    self._remove_answer_from_questionnaire_store(answer_id)

    def _remove_dependent_answers_from_completed_blocks(self, answer_id):
        """
        Gets a list of answers ids that are dependent on the answer_id passed in.
        Then for each dependent answer it will remove it's block from those completed.
        This will therefore force the respondent to revisit that block.
        The dependent answers themselves remain untouched.
        :param answer_id: the answer that has changed
        :return: None
        """
        answer_in_repeating_group = self._schema.answer_is_in_repeating_group(answer_id)
        dependencies = self._schema.answer_dependencies[answer_id]
        group_instance = self._current_location.group_instance

        for dependency in dependencies:
            dependency_in_repeating_group = self._schema.answer_is_in_repeating_group(dependency)

            answer = self._schema.get_answer(dependency)
            question = self._schema.get_question(answer['parent_id'])
            block = self._schema.get_block(question['parent_id'])

            if dependency_in_repeating_group and not answer_in_repeating_group:
                self._questionnaire_store.remove_completed_blocks(group_id=block['parent_id'], block_id=block['id'])
            else:
                location = Location(block['parent_id'], group_instance, block['id'])
                if location in self._questionnaire_store.completed_blocks:
                    self._questionnaire_store.remove_completed_blocks(location=location)

    def _remove_answer_from_questionnaire_store(self, answer_id):
        group_instance = self._current_location.group_instance or 0
        self._answer_store.remove(answer_ids=[answer_id],
                                  group_instance=group_instance,
                                  answer_instance=0)

    def _household_answers_changed(self, form):
        answer_ids = self._schema.get_answer_ids_for_block('household-composition')
        household_answers = self._answer_store.filter(answer_ids)

        del form['csrf_token']

        remove = [k for k in form if 'action[' in k]

        for k in remove:
            del form[k]

        if household_answers.count() != len(form):
            return True

        for household_answer in household_answers:
            answer = self._get_answer_instance_id(household_answer.get('answer_id'), household_answer.get('answer_instance', 0))

            if household_answer and (household_answer['value'] or '') != form[answer]:
                return True

        return False

    def remove_repeats_for_changed_household_answers(self, form):

        if self._household_answers_changed(form):
            answer_ids = self._schema.get_answer_ids_for_block('household-composition')
            self._answer_store.remove(answer_ids=answer_ids)

            for answer in self._schema.get_answers_that_repeat_in_block('household-composition'):
                groups_to_delete = self._schema.get_groups_that_repeat_with_answer_id(answer['id'])
                for group in groups_to_delete:
                    answer_ids = self._schema.get_answer_ids_for_group(group['id'])
                    self._answer_store.remove(answer_ids=answer_ids)
                    self._questionnaire_store.completed_blocks[:] = [b for b in self._questionnaire_store.completed_blocks if
                                                                     b.group_id != group['id']]

    def remove_empty_household_members(self):
        answer_ids = self._schema.get_answer_ids_for_block('household-composition')
        household_answers = self._answer_store.filter(answer_ids=answer_ids)
        household_member_name = defaultdict(list)
        for household_answer in household_answers:
            if household_answer['answer_id'] == 'first-name' or household_answer['answer_id'] == 'last-name':
                household_member_name[household_answer['answer_instance']].append(household_answer['value'])

        to_be_removed = []
        for k, v in household_member_name.items():
            name_value = ''.join(v).strip()
            if not name_value:
                to_be_removed.append(k)

        for instance_to_remove in to_be_removed:
            self._answer_store.remove(answer_ids=answer_ids, answer_instance=instance_to_remove)

    @staticmethod
    def _get_answer_instance_id(answer_id, answer_index):
        return 'household-{}-{}'.format(answer_index, answer_id)

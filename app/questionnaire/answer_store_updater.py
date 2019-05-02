from app.data_model.answer_store import Answer


class AnswerStoreUpdater:
    """ Component responsible for any actions that need to happen as a result of updating the answer store
    """

    EMPTY_ANSWER_VALUES = (None, [], '')

    def __init__(self, current_location, schema, questionnaire_store, current_question):
        self._current_location = current_location
        self._current_question = current_question or {}
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._answer_store = self._questionnaire_store.answer_store

    def save_answers(self, form):
        self._update_questionnaire_store_with_form_data(form.data)

        if self._current_location not in self._questionnaire_store.completed_blocks:
            self._questionnaire_store.completed_blocks.append(self._current_location)

        self._questionnaire_store.add_or_update()

    async def save_answers_async(self, form):
        self._update_questionnaire_store_with_form_data(form.data)

        if self._current_location not in self._questionnaire_store.completed_blocks:
            self._questionnaire_store.completed_blocks.append(self._current_location)

        await self._questionnaire_store.add_or_update_async()

    def _update_questionnaire_store_with_form_data(self, form_data):
        answer_ids_for_question = self._schema.get_answer_ids_for_question(self._current_question)

        for answer_id, answer_value in form_data.items():

            # If answer is not answered then check for a schema specified default
            if answer_value in self.EMPTY_ANSWER_VALUES:
                answer = next((answer for answer in self._current_question.get('answers', []) if answer['id'] == answer_id), {})
                answer_value = answer.get('default')

            if answer_id in answer_ids_for_question:
                if answer_value not in self.EMPTY_ANSWER_VALUES:
                    answer = Answer(answer_id=answer_id,
                                    value=answer_value)

                    self._answer_store.add_or_update(answer)
                else:
                    self._answer_store.remove(answer_ids=[answer_id])

from flask import url_for

from app.views.handlers.question import Question
from app.views.contexts.question import build_question_context


class PrimaryPersonListCollector(Question):
    def __init__(self, *args):
        self._is_adding = False
        self._primary_person_id = None
        super().__init__(*args)

    def get_next_location_url(self):
        if self._is_adding:
            add_or_edit_url = url_for(
                'questionnaire.block',
                list_name=self.rendered_block['for_list'],
                block_id=self.rendered_block['add_or_edit_block']['id'],
                list_item_id=self._primary_person_id,
            )
            return add_or_edit_url

        return super().get_next_location_url()

    def get_context(self, form):
        return build_question_context(self.rendered_block, form)

    def handle_post(self, form):
        if (
            form.data[self.rendered_block['add_or_edit_answer']['id']]
            == self.rendered_block['add_or_edit_answer']['value']
        ):
            self._is_adding = True
            self.questionnaire_store_updater.update_answers(form)
            self._primary_person_id = self.questionnaire_store_updater.add_primary_person(
                self.rendered_block['for_list']
            )
            # To ensure answering 'No' doesn't allow the user to skip ahead.
            self.questionnaire_store_updater.remove_completed_location()
            self.questionnaire_store_updater.save()
        else:
            self.questionnaire_store_updater.remove_primary_person(
                self.rendered_block['for_list']
            )
            return super().handle_post(form)

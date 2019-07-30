from flask import url_for

from app.views.handlers.question import Question
from app.views.contexts.list_collector import build_list_collector_context


class ListCollector(Question):
    def __init__(self, *args):
        self._is_adding = False
        super().__init__(*args)

    def get_next_location_url(self):
        if self._is_adding:
            add_url = url_for(
                'questionnaire.block',
                list_name=self.rendered_block['for_list'],
                block_id=self.rendered_block['add_block']['id'],
            )
            return add_url

        return super().get_next_location_url()

    def get_context(self, form):
        return build_list_collector_context(
            self.rendered_block,
            form,
            self._questionnaire_store.list_store,
            self._questionnaire_store.answer_store,
        )

    def handle_post(self, form):
        if (
            form.data[self.rendered_block['add_answer']['id']]
            == self.rendered_block['add_answer']['value']
        ):
            self._is_adding = True
            self.questionnaire_store_updater.update_answers(form)
            self.questionnaire_store_updater.save()
        else:
            return super().handle_post(form)

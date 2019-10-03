from flask import url_for
from werkzeug.utils import cached_property
from app.helpers.template_helper import safe_content

from app.questionnaire.location import Location
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.schema_utils import transform_variants
from app.views.contexts.list_collector import build_list_items_summary_context
from app.views.contexts.question import build_question_context
from app.views.handlers.block import BlockHandler


class Question(BlockHandler):
    @staticmethod
    def _has_redirect_to_list_add_action(answer_action):
        return answer_action and answer_action['type'] == 'RedirectToListAddQuestion'

    @cached_property
    def rendered_block(self):
        return self._render_block(self.block['id'])

    def get_next_location_url(self):
        answer_action = self._get_answer_action()
        if self._has_redirect_to_list_add_action(answer_action):
            location_url = self._get_list_add_question_url(answer_action['params'])

            if location_url:
                return location_url

        return self.router.get_next_location_url(
            self._current_location, self._routing_path
        )

    def _get_list_add_question_url(self, params):
        list_name = params['list_name']
        is_list_empty = not self._questionnaire_store.list_store[list_name].items

        if is_list_empty:
            block_id = params['block_id']
            section_id = self._schema.get_section_id_for_block_id(block_id)

            return Location(
                section_id=section_id, block_id=block_id, list_name=list_name
            ).url(previous=self.current_location.block_id)

    def _get_answer_action(self):
        answers = self.rendered_block['question']['answers']

        for answer in answers:
            submitted_answer = self.form.data[answer['id']]

            for option in answer.get('options', {}):
                action = option.get('action')

                if action and (
                    option['value'] == submitted_answer
                    or option['value'] in submitted_answer
                ):
                    return action

    def get_context(self):
        context = build_question_context(self.rendered_block, self.form)
        context['return_to_hub_url'] = self.get_return_to_hub_url()

        if 'list_items' in self.rendered_block:
            context['list_items'] = self.rendered_block['list_items']
        return context

    def handle_post(self):
        self.questionnaire_store_updater.update_answers(self.form)

        self.questionnaire_store_updater.add_completed_location()

        if self.questionnaire_store_updater.is_dirty:
            self._routing_path = self.path_finder.routing_path(
                section_id=self._current_location.section_id,
                list_item_id=self._current_location.list_item_id,
            )

        self._update_section_completeness()

        self.questionnaire_store_updater.save()

    @cached_property
    def questionnaire_store_updater(self):
        if not self._questionnaire_store_updater:
            self._questionnaire_store_updater = QuestionnaireStoreUpdater(
                self._current_location,
                self._schema,
                self._questionnaire_store,
                self.rendered_block.get('question'),
            )
        return self._questionnaire_store_updater

    def _render_block(self, block_id):
        block_schema = self._schema.get_block(block_id)

        variant_block = transform_variants(
            block_schema,
            self._schema,
            self._questionnaire_store.metadata,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._current_location,
        )

        self.page_title = self._get_page_title(variant_block)

        variant_question = variant_block.pop('question')
        rendered_question = self.placeholder_renderer.render(
            variant_question, self._current_location.list_item_id
        )

        response = {**variant_block, **{'question': rendered_question}}

        if 'list_summary' in variant_question:
            list_summary_context = build_list_items_summary_context(
                block_schema['question']['list_summary'],
                self._schema,
                self._questionnaire_store.answer_store,
                self._questionnaire_store.list_store,
                self._language,
            )
            response['list_items'] = list_summary_context

        return response

    def get_return_to_hub_url(self):
        if (
            self.rendered_block['type'] in ['Question', 'ConfirmationQuestion']
            and self._router.can_access_hub()
        ):
            return url_for('.get_questionnaire')

    def _get_page_title(self, transformed_block):
        question = transformed_block.get('question')
        if question:
            if isinstance(question['title'], str):
                question_title = question['title']
            else:
                question_title = question['title']['text']

            page_title = f'{question_title} - {self._schema.json["title"]}'

            return safe_content(page_title)

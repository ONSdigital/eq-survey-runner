from typing import List

from app.views.handlers.question import Question
from app.views.contexts.question import build_question_context
from app.questionnaire.location import Location


class ListAction(Question):
    @property
    def parent_block(self):
        return self._schema.get_block(self.block['parent_id'])

    @property
    def parent_location(self):
        return Location(
            section_id=self._current_location.section_id,
            block_id=self.rendered_block['parent_id'],
        )

    def is_location_valid(self):
        can_access_parent_location = self.router.can_access_location(
            self.parent_location, self._routing_path
        )

        if (
            not can_access_parent_location
            or self._current_location.list_name != self.parent_block['for_list']
        ):
            return False

        return True

    def get_previous_location_url(self):
        block_id = self._request_args.get('previous') or self._request_args.get(
            'return_to'
        )
        return self._get_location_url(block_id)

    def get_next_location_url(self):
        block_id = self._request_args.get('return_to')
        return self._get_location_url(block_id)

    def get_context(self):
        return build_question_context(self.rendered_block, self.form)

    def handle_post(self):
        # Clear the answer from the confirmation question on the list collector question
        answer_ids_to_remove = self._schema.get_answer_ids_for_block(
            self.parent_location.block_id
        )
        self.questionnaire_store_updater.remove_answers(answer_ids_to_remove)
        self.evaluate_sections()
        self.questionnaire_store_updater.save()

    def evaluate_sections(self):
        sections_to_evaluate = self._sections_to_evaluate()
        section_paths = self._routing_paths(sections_to_evaluate)
        for section_path in section_paths:
            self._update_section_completeness(
                Location(section_path[0][0]), section_path[1]
            )

    def _sections_to_evaluate(self):
        list_name = self._schema.get_block(self.rendered_block['parent_id'])['for_list']
        associated_sections = self._schema.get_sections_associated_to_list_name(
            list_name
        )
        associated_sections = {(element, None) for element in associated_sections}
        return self.questionnaire_store_updater.sections_to_evaluate(
            associated_sections
        )

    def _routing_paths(self, sections_to_evaluate: List[str]):
        return [
            (section_id, self.path_finder.routing_path(section_id[0]))
            for section_id in sections_to_evaluate
        ]

    def _get_location_url(self, block_id):
        if block_id and self._schema.is_block_valid(block_id):
            section_id = self._schema.get_section_id_for_block_id(block_id)
            return Location(section_id=section_id, block_id=block_id).url()

        return self.parent_location.url()

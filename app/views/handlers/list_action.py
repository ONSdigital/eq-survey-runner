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
        self.questionnaire_store_updater.save()

    def _get_location_url(self, block_id):
        if block_id and self._schema.is_block_valid(block_id):
            section_id = self._schema.get_section_id_for_block_id(block_id)
            return Location(section_id=section_id, block_id=block_id).url()

        return self.parent_location.url()

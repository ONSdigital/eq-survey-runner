from app.views.handlers.list_action import ListAction


class ListAddQuestion(ListAction):
    def is_location_valid(self):
        if not super().is_location_valid() or self._current_location.list_item_id:
            return False
        return True

    def handle_post(self, form):
        self.questionnaire_store_updater.add_list_item_and_answers(
            form, self.parent_block['for_list']
        )
        self.questionnaire_store_updater.update_answers(form)

        return super().handle_post(form)

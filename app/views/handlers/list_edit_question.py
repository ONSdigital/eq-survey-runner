from app.views.handlers.list_action import ListAction


class ListEditQuestion(ListAction):
    def is_location_valid(self):
        list_item_doesnt_exist = (
            self._current_location.list_item_id
            not in self._questionnaire_store.list_store[
                self._current_location.list_name
            ].items
        )
        if not super().is_location_valid() or list_item_doesnt_exist:
            return False
        return True

    def handle_post(self):
        self.questionnaire_store_updater.update_answers(self.form)

        return super().handle_post()

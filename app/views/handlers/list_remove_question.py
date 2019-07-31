from app.views.handlers.list_action import ListAction


class ListRemoveQuestion(ListAction):
    def is_location_valid(self):
        list_item_doesnt_exist = (
            self._current_location.list_item_id
            not in self._questionnaire_store.list_store[
                self._current_location.list_name
            ].items
        )
        is_primary = (
            self._questionnaire_store.list_store[
                self._current_location.list_name
            ].primary_person
            == self._current_location.list_item_id
        )
        if not super().is_location_valid() or list_item_doesnt_exist or is_primary:
            return False
        return True

    def handle_post(self, form):
        if (
            form.data[self.parent_block['remove_answer']['id']]
            == self.parent_block['remove_answer']['value']
        ):
            list_name = self.parent_block['for_list']
            self.questionnaire_store_updater.remove_list_item_and_answers(
                list_name, self._current_location.list_item_id
            )

        return super().handle_post(form)

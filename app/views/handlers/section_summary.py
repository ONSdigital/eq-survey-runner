from app.views.handlers.summary import Summary


class SectionSummary(Summary):
    @property
    def rendered_block(self):
        return self._render_block(self.block['id'])

    def get_context(self):
        group = self._schema.get_group_for_block_id(self._current_location.block_id)
        section = self._schema.get_section(group['parent_id'])

        context = self.build_context([section])

        self.add_context_questions(context)

        context['summary'].update({'title': section.get('title')})

        return context

from app.views.handlers.block import BlockHandler


class Content(BlockHandler):
    def get_context(self, _):
        return {
            'block': self.rendered_block,
            'metadata': dict(self._questionnaire_store.metadata),
        }

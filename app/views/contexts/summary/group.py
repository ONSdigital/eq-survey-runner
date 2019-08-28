from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.summary.block import Block


class Group:
    def __init__(
        self, group_schema, path, answer_store, list_store, metadata, schema, location
    ):
        self.id = group_schema['id']

        self.title = group_schema.get('title')

        self.location = location

        self.blocks = self._build_blocks(
            group_schema, path, answer_store, list_store, metadata, schema, location
        )
        self.placeholder_renderer = PlaceholderRenderer(
            language='en', schema=schema, answer_store=answer_store, metadata=metadata
        )

    @staticmethod
    def _build_blocks(
        group_schema, path, answer_store, list_store, metadata, schema, location
    ):
        blocks = []

        block_ids_on_path = [location.block_id for location in path]

        for block in group_schema['blocks']:
            if block['id'] in block_ids_on_path and block['type'] == 'Question':
                blocks.extend(
                    [
                        Block(
                            block, answer_store, list_store, metadata, schema, location
                        ).serialize()
                    ]
                )

        return blocks

    def serialize(self):
        return self.placeholder_renderer.render(
            {'id': self.id, 'title': self.title, 'blocks': self.blocks}, self.location.list_item_id
        )

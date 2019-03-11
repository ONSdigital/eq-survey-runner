from app.templating.summary.block import Block
from app.templating.template_renderer import renderer
from app.questionnaire.placeholder_renderer import PlaceholderRenderer


class Group:

    def __init__(self, group_schema, path, answer_store, metadata, schema, schema_context):
        self.id = group_schema['id']
        self.schema_context = schema_context
        self.answer_store = answer_store
        self.metadata = metadata

        self.title = group_schema.get('title')

        self.blocks = self._build_blocks(group_schema, path, answer_store, metadata, schema)

    @staticmethod
    def _build_blocks(group_schema, path, answer_store, metadata, schema):
        blocks = []

        block_ids_on_path = [location.block_id for location in path]

        for block in group_schema['blocks']:
            if block['id'] in block_ids_on_path and block['type'] == 'Question':
                blocks.extend([Block(block, answer_store, metadata, schema).serialize()])

        return blocks

    def serialize(self):

        group = {
            'id': self.id,
            'title': self.title,
            'blocks': self.blocks,
        }

        placeholder_renderer = PlaceholderRenderer(group, answer_store=self.answer_store, metadata=self.metadata)

        replaced_group = placeholder_renderer.render()

        return renderer.render(
            replaced_group,
            **self.schema_context
        )

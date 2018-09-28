from copy import deepcopy

from app.templating.summary.block import Block
from app.helpers.schema_helpers import get_group_instance_id
from app.questionnaire.location import Location
from app.templating.template_renderer import renderer


class Group:

    def __init__(self, group_schema, path, answer_store, metadata, schema, group_instance, schema_context):
        self.id = group_schema['id'] + '-' + str(group_instance)
        self.schema_context = schema_context

        location = Location(group_schema['id'], group_instance, group_schema['blocks'][0]['id'])
        self.group_instance_id = get_group_instance_id(schema, answer_store, location)

        self.title = self._get_title(group_schema, schema, answer_store, group_instance)

        self.blocks = self._build_blocks(group_schema, path, answer_store, metadata, schema, group_instance)

    @staticmethod
    def _build_blocks(group_schema, path, answer_store, metadata, schema, group_instance):
        blocks = []

        block_ids_on_path = [location.block_id for location in path if location.group_id == group_schema['id'] and location.group_instance == group_instance]

        for block in group_schema['blocks']:
            if block['id'] in block_ids_on_path and \
                    block['type'] == 'Question':
                blocks.extend([Block(block, group_schema['id'], answer_store, metadata, schema, group_instance).serialize()])

        return blocks

    def _get_title(self, group_schema, schema, answer_store, group_instance):
        section = schema.get_section(schema.get_group(group_schema['id'])['parent_id'])
        answer_values = []
        title_answer_ids = section.get('title_from_answers', [])

        for answer_id in title_answer_ids:
            for answer in answer_store.filter(answer_ids=[answer_id],
                                              group_instance_id=self.group_instance_id).escaped():
                if answer['value']:
                    answer_values.append(answer['value'])

        if answer_values:
            return ' '.join(answer_values)

        if group_instance == 0:
            return group_schema.get('title')

    def serialize(self):
        schema_context_with_group_instance_id = deepcopy(self.schema_context)
        schema_context_with_group_instance_id['group_instance_id'] = self.group_instance_id

        return renderer.render(
            {
                'id': self.id,
                'title': self.title,
                'blocks': self.blocks,
            },
            **schema_context_with_group_instance_id
        )

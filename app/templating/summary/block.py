from app.templating.summary.section import Section


class Block:

    def __init__(self, block_schema, answers, group_id, metadata, url_for):
        self.id = block_schema['id']
        self.title = block_schema['title'] if 'title' in block_schema else None
        self.sections = self._build_sections(block_schema, answers, group_id, metadata, url_for)

    @staticmethod
    def _build_sections(block_schema, answers, group_id, metadata, url_for):
        sections = []
        link = url_for('questionnaire.get_block',
                       eq_id=metadata['eq_id'],
                       form_type=metadata['form_type'],
                       collection_id=metadata['collection_exercise_sid'],
                       group_id=group_id,
                       group_instance=0,
                       block_id=block_schema['id'])

        sections.extend([Section(section, answers, link) for section in block_schema['sections']])

        return sections

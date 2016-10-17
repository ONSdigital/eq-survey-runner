import logging

from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
from app.templating.summary.summary_section import SummarySection

logger = logging.getLogger(__name__)


class SummaryTemplatePreprocessor(object):

    def build_view_data(self, node, schema, state_items):

        metadata_template_preprocessor = MetaDataTemplatePreprocessor()

        render_data = {
            "meta": metadata_template_preprocessor.build_metadata(schema),
            "content": self.build_summary_data(node, schema, state_items),
        }

        logger.debug("Rendering data is %s", render_data)

        return render_data

    @staticmethod
    def build_summary_data(node, schema, state_items):
        # An array of the sections to be shown on the summary page and their contents
        summary_sections = []

        for state in state_items:
            if state.display_on_summary:
                for section in state.sections:
                    section_schema = schema.get_item_by_id(section.id)
                    summary_section = SummarySection(section_schema, section)
                    summary_sections.append(summary_section)
        return summary_sections

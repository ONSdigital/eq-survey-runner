import logging

from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
from app.templating.summary.summary_section import SummarySection

logger = logging.getLogger(__name__)


class SummaryTemplatePreprocessor(object):

    def build_view_data(self, node, schema):

        metadata_template_preprocessor = MetaDataTemplatePreprocessor()

        render_data = {
            "meta": metadata_template_preprocessor.build_metadata(schema),
            "content": self.build_summary_data(node, schema),
        }

        logger.debug("Rendering data is %s", render_data)

        return render_data

    @staticmethod
    def build_summary_data(node, schema):
        # An array of the sections to be shown on the summary page and their contents
        summary_sections = []

        while node:
            # Not all nodes (pages) will have sections e.g. Introduction
            if node.state.display_on_summary:
                for section in node.state.sections:
                    section_schema = schema.get_item_by_id(section.id)
                    summary_section = SummarySection(section_schema, section)
                    summary_sections.append(summary_section)
            node = node.next
        return summary_sections

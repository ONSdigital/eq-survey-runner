import logging

from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
from app.templating.summary.block import Block as SummaryBlock


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

    def build_summary_data(self, node, schema):
        summary_blocks = []

        if node.state.display_on_summary:
            summary_blocks.append(SummaryBlock(schema.get_item_by_id(node.item_id), node.state))

        while node.next:
            node = node.next
            if node.state.display_on_summary:
                summary_blocks.append(SummaryBlock(schema.get_item_by_id(node.item_id), node.state))
        return summary_blocks

import logging

from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor


logger = logging.getLogger(__name__)


class SummaryTemplatePreprocessor(object):

    def build_view_data(self, node, schema):

        metadata_template_preprocessor = MetaDataTemplatePreprocessor()

        render_data = {
            "meta": metadata_template_preprocessor.build_metadata(schema),
            "content": self._get_states(node),
        }

        logger.debug("Rendering data is %s", render_data)

        return render_data

    def _get_states(self, node):
        # collection of states (essentially populated blocks)
        states = [node.state]

        while node.next:
            node = node.next
            if node.state.display_on_summary:
                states.append(node.state)
        return states

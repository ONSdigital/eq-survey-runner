from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor
import logging


logger = logging.getLogger(__name__)


class QuestionnaireTemplatePreprocessor(object):

    def build_view_data(self, node, schema):
        state = node.state

        metadata_template_preprocessor = MetaDataTemplatePreprocessor()

        render_data = {
            "meta": metadata_template_preprocessor.build_metadata(schema),
            "content": state
        }

        logger.debug("Rendering data is %s", render_data)

        return render_data

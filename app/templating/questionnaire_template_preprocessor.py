import logging

from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor

logger = logging.getLogger(__name__)


class QuestionnaireTemplatePreprocessor(object):

    def build_view_data(self, node, schema, state_items):

        metadata_template_preprocessor = MetaDataTemplatePreprocessor()
        render_data = {
            "meta": metadata_template_preprocessor.build_metadata(schema),
            "content": state_items[0],
        }

        logger.debug("Rendering data is %s", render_data)

        return render_data

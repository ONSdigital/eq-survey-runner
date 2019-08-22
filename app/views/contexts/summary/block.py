from app.questionnaire.rules import evaluate_when_rules
from app.views.contexts.summary.question import Question


class Block:
    @staticmethod
    def get_question(
        block_schema, answer_store, list_store, metadata, schema, current_location=None
    ):
        """ Taking question variants into account, return the question which was displayed to the user """
        for variant in block_schema.get('question_variants', []):
            display_variant = evaluate_when_rules(
                variant.get('when'),
                schema,
                metadata,
                answer_store,
                list_store,
                current_location,
            )
            if display_variant:
                return Question(variant['question'], answer_store, schema).serialize()

        return Question(block_schema['question'], answer_store, schema).serialize()

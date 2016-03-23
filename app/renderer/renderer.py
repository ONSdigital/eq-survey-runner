from collections import OrderedDict
from app.model.response import Response


class Renderer(object):
    def __init__(self, schema, response_store, validation_store):
        self._schema = schema
        self._response_store = response_store
        self._validation_store = validation_store

    def render(self):
        self._augment_responses()
        self._augment_questionnaire()

        template_vars = {
            "data": self._schema
        }

        return template_vars

    def _augment_responses(self):
        # Augment the schema with user responses and validation results
        for item_id, item in self._schema.items_by_id.items():
            if isinstance(item, Response):
                item.value = self._response_store.get_response(item.id)
                validation_result = self._validation_store.get_result(item.id)
                if validation_result:
                    item.is_valid = validation_result.is_valid
                    item.errors = validation_result.get_errors()
                    item.warnings = validation_result.get_warnings()
                else:
                    item.is_valid = None
                    item.errors = None
                    item.warnings = None

    def _augment_questionnaire(self):
        errors = OrderedDict()
        warnings = OrderedDict()

        # loops through the Schema and get errors and warnings in order
        for group in self._schema.groups:
            group_result = self._validation_store.get_result(group.id)
            if group_result and not group_result.is_valid:
                errors[group.id] = group_result.errors
                warnings[group.id] = group_result.warnings

            for block in group.blocks:
                block_result = self._validation_store.get_result(block.id)
                if block_result and not block_result.is_valid:
                    errors[block.id] = block_result.errors
                    warnings[block.id] = block_result.warnings

                for section in block.sections:
                    section_result = self._validation_store.get_result(section.id)
                    if section_result and not section_result.is_valid:
                        errors[section.id] = section_result.errors
                        warnings[section.id] = section_result.warnings

                    for question in section.questions:
                        question_result = self._validation_store.get_result(question.id)
                        if question_result and not question_result.is_valid:
                            errors[question.id] = question_result.errors
                            warnings[question.id] = question_result.warnings

                        for response in question.responses:
                            response_result = self._validation_store.get_result(response.id)
                            if response_result and not response_result.is_valid:
                                errors[response.id] = response_result.errors
                                warnings[response.id] = response_result.warnings

        self._schema.errors = errors
        self._schema.warnings = warnings

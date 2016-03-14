from app.validation.validation_result import ValidationResult
from app.validation.required import Required


class ValidationException(Exception):
    pass


class Validator(object):
    def __init__(self, schema, validation_store, response_store):
        self._schema = schema
        self._validation_store = validation_store
        self._response_store = response_store

    def validate(self, user_data):
        for item_id in user_data.keys():
            item = self.schema.get_item_by_id(item_id)

            if not item:
                raise ValidationException('{} is not a known item'.format(item_id))

            self._validation_store.store_result(item_id,
                                                self._validate_item(item, user_data[item_id]))

            self._validate_container(item.container)

    def _validate_item(self, item, item_data):
        # Do "required" check
        if item.required:
            result = self._required_check(item, item_data)
            if not result.is_valid:
                return result

        # Implicit -type-checking
        result = self._type_check(item, item_data)
        if not result.is_valid:
            return result

        # check for additional validation rules
        if item.validation:
            for rule in item.validation:
                result = rule.validate(item_data, self._response_store)
                if not result.is_valid:
                    return result

        # If we've made it this far, the thing is valid
        return ValidationResult(True)

    def _validate_container(self, item):
        if item and item.validation:
            for rule in item.validation:
                result = rule.validate(None, self._response_store)
                if not result.is_valid:
                    self._validation_store.store_result(item.id, result)
                    return

            self._validation_store.store_result(item.id, ValidationResult(True))

            self._validate_container(item.container)

    def _required_check(self, item, item_data):
        required = Required()
        result = required.validate(item_data)
        if not result.is_valid:
            return result
        return ValidationResult(True)

    def _type_check(self, item, item_data):
        validators = self._type_validator_factory_class.get_validators_by_type(item.type)

        for validator in validators:
            result = validator.validate(item_data)
            if not result.is_valid:
                return result

        return ValidationResult(True)

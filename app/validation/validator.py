from app.validation.validation_result import ValidationResult
from app.validation.mandatory_check import MandatoryCheck
from app.validation.type_validator_factory import TypeValidatorFactory
from app.validation.abstract_validator import AbstractValidator
from flask.ext.babel import gettext as _
import logging


logger = logging.getLogger(__name__)


class ValidationException(Exception):
    pass


class Validator(object):
    def __init__(self, schema, validation_store, response_store):
        self._schema = schema
        self._validation_store = validation_store
        self._response_store = response_store

        # Set the factory class here, so we can override it for tests
        self._type_validator_factory_class = TypeValidatorFactory

        # Set up default error and warning messages
        self.messages = {
            AbstractValidator.NOT_INTEGER: _("This is not a whole number"),
            AbstractValidator.NOT_STRING: _("This is not a string"),
            AbstractValidator.MANDATORY: _("This field is mandatory"),
            AbstractValidator.INVALID_DATE: _("This is not a valid date"),
            AbstractValidator.NEGATIVE_INTEGER: _("Negative values are not allowed"),
            AbstractValidator.INTEGER_TOO_LARGE: _('This number is too big')
        }

    def validate(self, user_data):
        for item_id in user_data.keys():
            logger.debug('Attempting to validate {}'.format(item_id))
            item = self._schema.get_item_by_id(item_id)

            # Currently the datefields trip this up
            if not item:
                logger.info('Ignoring {}'.format(item_id))
                # raise ValidationException('{} is not a known item'.format(item_id))
                continue

            result = self._validate_item(item, user_data[item_id])
            logger.debug('Item {} ({}) valid: {}'.format(item_id, type(item), result.is_valid))
            self._validation_store.store_result(item_id, result)

            self._validate_container(item.container)

        # Return true/False for the set of values
        for item_id in user_data.keys():
            result = self._validation_store.get_result(item_id)
            if result:
                if not result.is_valid:
                    return False

        return True

    def _validate_item(self, item, item_data):
        # Do "mandatory" check
        if item.mandatory:
            logger.debug('Item ({}) is mandatory, data is: {}'.format(item.id, item_data))
            result = self._mandatory_check(item, item_data)
            if not result.is_valid:
                self._update_messages(item, result)
                return result

        # Validate if data is present
        if item_data:
            # Implicit -type-checking
            logger.debug('Type Checking ({}) with data {}'.format(item.id, item_data))
            result = self._type_check(item, item_data)
            if not result.is_valid:
                self._update_messages(item, result)
                return result

            # check for additional validation rules
            if item.validation:
                for rule in item.validation:
                    result = rule.validate(item_data, self._response_store)
                    if not result.is_valid:
                        self._update_messages(item, result)
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

    def _mandatory_check(self, item, item_data):
        mandatory = MandatoryCheck()
        result = mandatory.validate(item_data)
        if not result.is_valid:
            self._update_messages(item, result)
            return result
        return ValidationResult(True)

    def _type_check(self, item, item_data):
        validators = self._type_validator_factory_class.get_validators_by_type(item.type)

        for validator in validators:
            result = validator.validate(item_data)
            if not result.is_valid:
                self._update_messages(item, result)
                return result

        return ValidationResult(True)

    def _update_messages(self, item, result):
        # error messages
        for index, code in enumerate(result.errors):
            if code in item.messages.keys():
                result.errors[index] = item.messages[code]
            elif code in self.messages.keys():
                # Use the default error message
                result.errors[index] = self.messages[code]

        # warning messages
        for index, code in enumerate(result.warnings):
            if code in item.messages.keys():
                result.warnings[index] = item.messages[code]
            elif code in self.messages.keys():
                # Use the default error message
                result.warnings[index] = self.messages[code]

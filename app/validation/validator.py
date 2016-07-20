from app.validation.validation_result import ValidationResult
from app.validation.mandatory_check import MandatoryCheck
from app.validation.type_validator_factory import TypeValidatorFactory
from app.validation.abstract_validator import AbstractValidator
from app.schema.answer import Answer
from flask.ext.babel import gettext as _
from app.schema.questionnaire import QuestionnaireException
import logging


logger = logging.getLogger(__name__)


class ValidationException(Exception):
    pass


class Validator(object):
    def __init__(self, schema, validation_store, user_journey_manager):
        self._schema = schema
        self._validation_store = validation_store
        self._user_journey_manager = user_journey_manager

        # Set the factory class here, so we can override it for tests
        self._type_validator_factory_class = TypeValidatorFactory

        # Set up default error and warning messages
        self.messages = {
            AbstractValidator.NOT_INTEGER: _("Please only enter whole numbers into the field."),
            AbstractValidator.NOT_STRING: _("This is not a string."),
            AbstractValidator.MANDATORY: _("This field is mandatory."),
            AbstractValidator.INVALID_DATE: _("This is not a valid date."),
            AbstractValidator.NEGATIVE_INTEGER: _("Negative values are not allowed."),
            AbstractValidator.INTEGER_TOO_LARGE: _('This number is too big.'),
            AbstractValidator.INVALID_DATE_RANGE_TO_BEFORE_FROM: _("The 'to' date cannot be before the 'from' date."),
            AbstractValidator.INVALID_DATE_RANGE_TO_FROM_SAME: _("The 'to' date must be different to the 'from' date.")
        }

    def validate(self, user_data):

        for item_id in user_data.keys():
            logger.debug('Attempting to validate {}'.format(item_id))
            try:
                item = self._schema.get_item_by_id(item_id)

                result = self._validate_item(item, user_data[item_id])
                logger.debug('Item {} ({}) valid: {}'.format(item_id, type(item), result.is_valid))
                self._validation_store.store_result(item_id, result)

                if result.is_valid:
                    self._validate_container(item.container, user_data)
            except QuestionnaireException:
                pass

        # Return true/False for the set of values
        for item_id in user_data.keys():
            try:
                result = self._validation_store.get_result(item_id)
                item = self._schema.get_item_by_id(item_id)
                container_result = self._validation_store.get_result(item.container.id)

                if result:
                    if not result.is_valid or (container_result and not container_result.is_valid):
                        return False
            except QuestionnaireException:
                pass

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
            # check for additional validation rules
            if item.validation:
                for rule in item.validation:
                    result = rule.validate(item_data, self._user_journey_manager)
                    if not result.is_valid:
                        self._update_messages(item, result)
                        return result

        # If we've made it this far, the thing is valid
        return ValidationResult(True)

    def _validate_container(self, item, user_data):

        # only type check container if all parts are present and valid
        children_user_data = []
        for child in item.children:
            child_result = self._validation_store.get_result(child.id)
            if child_result and child_result.is_valid:
                children_user_data.append(user_data[child.id])
            else:
                return

        result = self._type_check(item, children_user_data)
        self._validation_store.store_result(item.id, result)

        if item and item.validation:
            for rule in item.validation:
                result = rule.validate(None, self._user_journey_manager)
                if not result.is_valid:
                    self._validation_store.store_result(item.id, result)
                    return

            self._validation_store.store_result(item.id, ValidationResult(True))

            self._validate_container(item.container, user_data)

    def _mandatory_check(self, item, item_data):
        mandatory = MandatoryCheck()
        result = mandatory.validate(item_data)
        if not result.is_valid:
            self._update_messages(item, result)
            return result
        return ValidationResult(True)

    def _type_check(self, item, item_data):
        validators = self._type_validator_factory_class.get_validators_by_type(item)

        for validator in validators:
            result = validator.validate(item_data)

            if not result.is_valid:
                self._update_messages(item, result)
                return result

        return ValidationResult(True)

    def _update_messages(self, item, result):
        # error messages
        for index, code in enumerate(result.errors):
            if isinstance(item, Answer) and code in item.messages.keys():
                result.errors[index] = item.messages[code]
            elif code in self.messages.keys():
                # Use the default error message
                result.errors[index] = self.messages[code]

        # warning messages
        for index, code in enumerate(result.warnings):
            if isinstance(item, Answer) and code in item.messages.keys():
                result.warnings[index] = item.messages[code]
            elif code in self.messages.keys():
                # Use the default error message
                result.warnings[index] = self.messages[code]

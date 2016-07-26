from app.validation.validation_result import ValidationResult
from app.validation.mandatory_check import MandatoryCheck
from app.validation.abstract_validator import AbstractValidator
from app.schema.questionnaire import QuestionnaireException
from app.schema.answer import Answer
from flask.ext.babel import gettext as _
import logging


logger = logging.getLogger(__name__)


class ValidationException(Exception):
    pass


class Validator(object):
    def __init__(self, schema, validation_store, user_journey_manager):
        self._schema = schema
        self._validation_store = validation_store
        self._user_journey_manager = user_journey_manager

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

    def validate(self):
        # get the current location in the questionnaire
        current_location = self._user_journey_manager.get_current_location()
        if self._user_journey_manager.is_valid_location(current_location):
            try:
                current_state = self._user_journey_manager.get_state(current_location)
                schema_item = self._schema.get_item_by_id(current_state.item_id)

                return schema_item.validate(current_state.page_state)
            except QuestionnaireException as e:
                # Item has state, but is not in schema: must be introduction, thank you or summary
                return True
        else:
            # Not a validation location, so can't be valid
            return False

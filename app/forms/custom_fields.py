from decimal import Decimal, InvalidOperation
from wtforms import TextAreaField, IntegerField, DecimalField


class MaxTextAreaField(TextAreaField):
    def __init__(self, label='', validators=None, maxlength=10000, **kwargs):
        super(MaxTextAreaField, self).__init__(label, validators, **kwargs)
        self.maxlength = maxlength


class CustomIntegerField(IntegerField):
    """
    The default wtforms field coerces data to an int and raises
    cast errors outside of it's validation chain. In order to stop
    the validation chain, we create a custom field that doesn't
    raise the error and we can instead fail and stop other calls to
    further validation steps by using a separate NumberCheck and
    DecimalPlace validators
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None

    def process_formdata(self, valuelist):

        if valuelist:
            try:
                self.data = int(valuelist[0])
            except ValueError:
                pass


class CustomDecimalField(DecimalField):
    """
    The default wtforms field coerces data to an number and raises
    cast errors outside of it's validation chain. In order to stop
    the validation chain, we create a custom field that doesn't
    raise the error and we can instead fail and stop other calls to
    further validation steps by using a separate NumberCheck and
    DecimalPlace validators
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None

    def process_formdata(self, valuelist):

        if valuelist:
            try:
                self.data = Decimal(valuelist[0])
            except (ValueError, TypeError, InvalidOperation):
                pass

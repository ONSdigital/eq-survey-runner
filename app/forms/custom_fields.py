from decimal import Decimal, InvalidOperation

from babel import numbers
from wtforms import (
    TextAreaField,
    IntegerField,
    DecimalField,
    SelectMultipleField,
    SelectField,
)

from app.settings import DEFAULT_LOCALE


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
                self.data = int(
                    valuelist[0].replace(numbers.get_group_symbol(DEFAULT_LOCALE), '')
                )
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
                self.data = Decimal(
                    valuelist[0].replace(numbers.get_group_symbol(DEFAULT_LOCALE), '')
                )
            except (ValueError, TypeError, InvalidOperation):
                pass


class CustomSelectMultipleField(SelectMultipleField):
    """
    This custom field allows us to add the additional detail_answer_id to choices/options.
    This saves us having to later map options with their detail_answer.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __iter__(self):
        opts = dict(
            widget=self.option_widget, _name=self.name, _form=None, _meta=self.meta
        )
        for i, (value, label, checked, detail_answer_id) in enumerate(
            self.iter_choices()
        ):
            opt = self._Option(label=label, id='%s-%d' % (self.id, i), **opts)
            opt.process(None, value)
            opt.detail_answer_id = detail_answer_id
            opt.checked = checked
            yield opt

    def iter_choices(self):
        for value, label, detail_answer_id in self.choices:
            selected = self.data is not None and self.coerce(value) in self.data
            yield (value, label, selected, detail_answer_id)


class CustomSelectField(SelectField):
    """
    This custom field allows us to add the additional detail_answer_id to choices/options.
    This saves us having to later map options with their detail_answer.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __iter__(self):
        opts = dict(
            widget=self.option_widget, _name=self.name, _form=None, _meta=self.meta
        )
        for i, (value, label, checked, detail_answer_id) in enumerate(
            self.iter_choices()
        ):
            opt = self._Option(label=label, id='%s-%d' % (self.id, i), **opts)
            opt.process(None, value)
            opt.detail_answer_id = detail_answer_id
            opt.checked = checked
            yield opt

    def iter_choices(self):
        for value, label, detail_answer_id in self.choices:
            yield (value, label, self.coerce(value) == self.data, detail_answer_id)

    def pre_validate(self, form):
        for value, _, _ in self.choices:
            if value == self.data:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))

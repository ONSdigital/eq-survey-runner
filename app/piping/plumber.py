import re


class Plumber(object):
    def __init__(self, context):
        self._context = context

    def plumb_item(self, item):
        interesting_properties = self.get_properties_of_interest(item)

        for interesting_property in interesting_properties:
            if self._needs_plumbing(item, interesting_property):
                self._plumb(item, interesting_property)

    def get_properties_of_interest(self, item):
        if hasattr(item, 'templatable_properties'):
            return item.templatable_properties
        else:
            return []

    def _needs_plumbing(self, item, interesting_property):
        value = getattr(item, interesting_property)
        pattern = re.compile("\{.+\}")
        needs_plumbing = pattern.search(value)
        if needs_plumbing is not None:
            return True
        return False

    def _plumb(self, item, interesting_property):
        if hasattr(item, interesting_property):
            template = getattr(item, interesting_property)
            formatting_data = self._context
            plumbed_value = template.format(**formatting_data)
            setattr(item, interesting_property, plumbed_value)

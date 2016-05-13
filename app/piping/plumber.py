from string import Template


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
        return '$' in value

    def _plumb(self, item, interesting_property):
        if hasattr(item, interesting_property):
            template = Template(getattr(item, interesting_property))
            plumbed_value = template.safe_substitute(self._context)
            setattr(item, interesting_property, plumbed_value)

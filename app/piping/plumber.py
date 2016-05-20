import re


class Plumber(object):
    def __init__(self, context):
        self._context = context

    def plumb_item(self, item):
        templatable_properties = item.templatable_properties

        for templatable_property in templatable_properties:
            if self._needs_plumbing(item, templatable_property):
                self._plumb(item, templatable_property)

    def _needs_plumbing(self, item, templatable_property):
        value = getattr(item, templatable_property)
        if value is not None:
            pattern = re.compile("\{.+\}")
            needs_plumbing = pattern.search(value)
            if needs_plumbing is not None:
                return True
        return False

    def _plumb(self, item, templatable_property):
        if hasattr(item, templatable_property):
            try:
                template = getattr(item, templatable_property)
                formatting_data = self._context
                plumbed_value = template.format(**formatting_data)
                setattr(item, templatable_property, plumbed_value)
            except KeyError:
                pass    # Do nothing, leave the propery as is

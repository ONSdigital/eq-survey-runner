import re
import logging


logger = logging.getLogger(__name__)


class Plumber(object):
    '''
    This class takes a dict of objects which contain values that can be piped into the author provided text of schema objects.
    e.g. Question Title "Hello {user.name}" is replaced by with the name property of the user object
    '''
    def __init__(self, context):
        self._context = context

    def plumb_item(self, item):
        '''
        Check an item for properties needing string replacement and replace where neccessary
        '''
        templatable_properties = item.templatable_properties

        for templatable_property in templatable_properties:
            if self._needs_plumbing(item, templatable_property):
                self._plumb(item, templatable_property)

    def _needs_plumbing(self, item, templatable_property):
        '''
        Returns a boolean indication of whether a string replacement is needed
        '''
        value = getattr(item, templatable_property)
        if value is not None:
            pattern = re.compile("\{.+\}")
            needs_plumbing = pattern.search(value)
            if needs_plumbing is not None:
                return True
        return False

    def _plumb(self, item, templatable_property):
        '''
        Perform the string replacement directly on the object
        '''
        if hasattr(item, templatable_property):
            logger.debug('Piping property "{}" of item "{}"'.format(templatable_property, item.id))
            template = getattr(item, templatable_property)
            try:
                formatting_data = self._context
                plumbed_value = template.format(**formatting_data)
                setattr(item, templatable_property, plumbed_value)
            except KeyError:
                logger.warn('Property "{}" of item "{}" cannot be piped'.format(templatable_property, item.id))
                pass    # Do nothing, leave the propery as is
            except Exception as e:
                logger.error('Data required to pip property "{}" of item "{}" is invalid.  The template is "{}"'.format(templatable_property, item.id, template))  # NOQA
                logger.exception(e)
                raise e

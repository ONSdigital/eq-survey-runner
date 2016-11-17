import json

from app.jinja_filters import format_date

from jinja2 import Environment


class TemplateRenderer:
    def __init__(self):
        self.environment = Environment()
        self.environment.filters['format_date'] = format_date

    def render(self, renderable, **context):
        """
        Substitute variables into renderable with the variables in context
        :param renderable: dict with variables to be substituted
        :param context: the variables to substitute
        :return: the rendered version of the original renderable dict
        """
        json_string = json.dumps(renderable)
        template = self.environment.from_string(json_string)
        rendered = template.render(**context)
        return json.loads(rendered)

    def render_state(self, state, context):
        """
        Substitute variables into state items recursively with the variables in context
        :param state: state with properties to be substituted
        :param context: the variables to substitute
        :return: the rendered version of the state
        """
        # plumb the state and then all its children
        if state.schema_item:
            templatable_properties = state.schema_item.templatable_properties
            for templatable_property in templatable_properties:
                template_string = getattr(state.schema_item, templatable_property)
                if template_string is not None:
                    plumbed_value = self.render(template_string, **context)
                    setattr(state.schema_item, templatable_property, plumbed_value)
        for child in state.children:
            self.render_state(child, context)
        return state

renderer = TemplateRenderer()

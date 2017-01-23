import json

from jinja2 import Environment

from app.jinja_filters import format_date, format_household_member_name, format_household_summary


class TemplateRenderer:
    def __init__(self):
        self.environment = Environment()
        self.environment.filters['format_date'] = format_date
        self.environment.filters['format_household_name'] = format_household_member_name
        self.environment.filters['format_household_summary'] = format_household_summary

    def render(self, renderable, **context):
        """
        Substitute variables into renderable with the variables in context
        :param renderable: dict with variables to be substituted
        :param context: the variables to substitute
        :return: the rendered version of the original renderable dict
        """
        json_string = json.dumps(renderable) if isinstance(renderable, dict) else renderable
        template = self.environment.from_string(json_string)
        rendered = template.render(**context)
        result = rendered if isinstance(renderable, dict) else json.dumps(rendered)
        return json.loads(result)

    def render_schema_items(self, schema_item, context):
        """
        Substitute variables into schema items recursively with the variables in context
        :param schema_item: schema with properties to be substituted
        :param context: the variables to substitute
        :return: the rendered version of the state
        """
        # plumb the state and then all its children
        if schema_item:
            templatable_properties = schema_item.templatable_properties
            for templatable_property in templatable_properties:
                self._set_property(context, schema_item, templatable_property)
        children = schema_item.children or []
        for child in children:
            self.render_schema_items(child, context)
        return schema_item

    def _set_property(self, context, schema_item, templatable_property):
        template_property = getattr(schema_item, templatable_property)
        if isinstance(template_property, list):
            properties = []
            list_of_dicts = [template_properties for template_properties in template_property if isinstance(template_properties, dict)]
            for template_property_item in list_of_dicts:
                plumbed_value = self.render(template_property_item, **context)
                properties.append(plumbed_value)
            setattr(schema_item, templatable_property, properties)
        else:
            if template_property is not None:
                plumbed_value = self.render(template_property, **context)
                setattr(schema_item, templatable_property, plumbed_value)


renderer = TemplateRenderer()

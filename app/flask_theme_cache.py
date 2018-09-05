import jinja2
import flask_themes2


path_cache = {}


def get_global_theme_template():
    def _get_templatepath(theme, templatename, fallback):
        cache_key = (theme, templatename, fallback)
        cache_value = path_cache.get(cache_key, None)
        if cache_value is not None:
            return cache_value

        templatepath = '_themes/{}/{}'.format(theme, templatename)
        if (not fallback) or flask_themes2.template_exists(templatepath):
            result = templatepath
        else:
            result = templatename

        path_cache[cache_key] = result
        return result

    @jinja2.contextfunction
    def global_theme_template(ctx, templatename, fallback=True):
        theme = flask_themes2.active_theme(ctx)
        return _get_templatepath(theme, templatename, fallback)

    return global_theme_template

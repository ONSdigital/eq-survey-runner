import jinja2
import flask_themes2


def get_global_theme_template(cache):
    @cache.memoize()
    def _get_templatepath(theme, templatename, fallback):
        templatepath = '_themes/{}/{}'.format(theme, templatename)
        if (not fallback) or flask_themes2.template_exists(templatepath):
            return templatepath

        return templatename

    @jinja2.contextfunction
    def global_theme_template(ctx, templatename, fallback=True):
        theme = flask_themes2.active_theme(ctx)
        return _get_templatepath(theme, templatename, fallback)

    return global_theme_template

KNOWN_TEMPLATES = {
    'introduction': {'template': "landing-page.html"},
    'summary': {'template': "summary.html"},
    'confirmation': {'template': "confirmation.html"},
    'thank-you': {'template': "thank-you.html"},
    'questionnaire': {'template': "questionnaire.html"},
}


class TemplateRegistry(object):

    @staticmethod
    def get_template_name(current_location):
        if current_location in KNOWN_TEMPLATES:
            return KNOWN_TEMPLATES[current_location]['template']
        else:
            # must be a valid location to get this far, so must be within the
            # questionnaire
            return KNOWN_TEMPLATES['questionnaire']['template']

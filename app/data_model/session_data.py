class SessionData(object):

    def __init__(self, tx_id, eq_id, form_type, period_str, language_code=None, survey_url=None, ru_name=None, ru_ref=None, submitted_time=None):
        self.tx_id = tx_id
        self.eq_id = eq_id
        self.form_type = form_type
        self.period_str = period_str
        self.ru_name = ru_name
        self.ru_ref = ru_ref
        self.submitted_time = submitted_time

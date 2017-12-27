class SessionData(object):

    def __init__(self, tx_id, eq_id, form_type, period_str, submitted_time=None):
        self.tx_id = tx_id
        self.eq_id = eq_id
        self.form_type = form_type
        self.period_str = period_str
        self.submitted_time = submitted_time

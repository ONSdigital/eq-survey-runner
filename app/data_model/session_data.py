class SessionData:

    def __init__(self,
                 tx_id,
                 eq_id,
                 form_type,
                 period_str,
                 language_code,
                 survey_url,
                 ru_name,
                 ru_ref,
                 case_id,
                 case_ref=None,
                 account_service_url=None,
                 submitted_time=None,
                 trad_as=None,
                 **_):                  # pylint: disable=too-many-locals
        self.tx_id = tx_id
        self.eq_id = eq_id
        self.form_type = form_type
        self.period_str = period_str
        self.language_code = language_code
        self.survey_url = survey_url
        self.ru_name = ru_name
        self.ru_ref = ru_ref
        self.submitted_time = submitted_time
        self.case_id = case_id
        self.case_ref = case_ref
        self.trad_as = trad_as
        self.account_service_url = account_service_url

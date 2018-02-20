from app.data_model.session_data import SessionData


class TestSessionData(SessionData):

    def __init__(self, tx_id, eq_id, form_type, period_str, language_code, survey_url, ru_name,
                 ru_ref, submitted_time=None, additional_value=None, second_additional_value=None):
        super().__init__(tx_id, eq_id, form_type, period_str, language_code, survey_url, ru_name, ru_ref,
                         submitted_time)

        self.additional_value = additional_value
        self.second_additional_value = second_additional_value

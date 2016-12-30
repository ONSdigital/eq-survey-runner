class MultipleChoiceHelper(object):

    @staticmethod
    def find_other_value(posted_data, options):
        """
        Compare the posted_data with the options in the schema, if there is a value which doesn't match
        the options it must be the other value
        """
        if posted_data and 'other' in (value.lower() for value in posted_data):
            for answer in posted_data:
                answer_in_options = any(option['value'] == answer for option in options)
                if answer and not answer.isspace() and not answer_in_options and answer.lower() != 'other':
                    return answer

        return None

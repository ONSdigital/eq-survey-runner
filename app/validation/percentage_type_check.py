from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck


class PercentageTypeCheck(PositiveIntegerTypeCheck):

    def __init__(self):
        super().__init__(0, 100)

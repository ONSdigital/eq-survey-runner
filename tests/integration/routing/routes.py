from tests.integration.routing import rules

ROUTES = (
            (
             rules.CHOOSE_A_SIDE_LIGHT_SIDE,
             rules.LIGHT_SHIP_NO,
             rules.QUIZ_PAGE_1,
             rules.QUIZ_PAGE_2,
             rules.QUIZ_PAGE_3
            ),
            (
             rules.CHOOSE_A_SIDE_LIGHT_SIDE,
             rules.LIGHT_SHIP_YES,
             rules.LIGHT_SHIP_PICK,
             rules.QUIZ_PAGE_1,
             rules.QUIZ_PAGE_2,
             rules.QUIZ_PAGE_3
            ),
            (
             rules.CHOOSE_A_SIDE_DARK_SIDE,
             rules.DARK_SHIP_YES,
             rules.DARK_SHIP_PICK,
             rules.QUIZ_PAGE_1,
             rules.QUIZ_PAGE_2,
             rules.QUIZ_PAGE_3
            ),
            (
             rules.CHOOSE_A_SIDE_DARK_SIDE,
             rules.DARK_SHIP_NO,
             rules.QUIZ_PAGE_1,
             rules.QUIZ_PAGE_2,
             rules.QUIZ_PAGE_3
            ),
            (
             rules.CHOOSE_A_SIDE_DARK_SIDE,
             rules.DARK_SHIP_PAIN,
             rules.LIGHT_SHIP_PICK,
             rules.QUIZ_PAGE_1,
             rules.QUIZ_PAGE_2,
             rules.QUIZ_PAGE_3
            )
        )


def get_all_routes():
    return ROUTES


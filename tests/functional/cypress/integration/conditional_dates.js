import {openQuestionnaire} from '../helpers/helpers.js'

const DatesPage = require('../../generated_pages/conditional_dates/date-block.page')
const DatesConfirmationPage = require('../../generated_pages/conditional_dates/date-value-test.page')
const SummaryPage = require('../../generated_pages/conditional_dates/summary.page')

describe('Piped Dates', function () {

  beforeEach(() => {
    openQuestionnaire('test_conditional_dates.json')
  })

  it('Given the test_conditional_dates survey is selected when dates are entered then the summary screen shows the dates entered, formatted', () => {
    cy
      .get(DatesPage.dateStartFromday()).type(11)
      .get(DatesPage.dateStartFrommonth()).select("10")
      .get(DatesPage.dateStartFromyear()).type(2017)
      .get(DatesPage.dateEndToday()).type(3)
      .get(DatesPage.dateEndTomonth()).select("12")
      .get(DatesPage.dateEndToyear()).type(2017)
      .get(DatesPage.submit()).click()
      .get(DatesConfirmationPage.dateTest()).type(1)
      .get(DatesConfirmationPage.submit()).click()

      // Then the summary screen shows the dates entered formatted
      .get(SummaryPage.totalRetailTurnoverQuestion()).should('have', '11 October 2017 to 3 December 2017')

  })

  it('Given the test_conditional_dates survey is selected when no dates are entered then the summary screen shows the default dates in the question', () => {
    cy
      .get(DatesPage.submit()).click()
      .get(DatesConfirmationPage.dateTest()).type(2)
      .get(DatesConfirmationPage.submit()).click()
      .get(SummaryPage.totalRetailTurnoverQuestion()).should('have', '1 January 2017 to 1 February 2017')
  })
})

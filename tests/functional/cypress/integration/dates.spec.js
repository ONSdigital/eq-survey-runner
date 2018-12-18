import {openQuestionnaire} from '../helpers/helpers.js'
const DatesPage = require('../../generated_pages/dates/date-block.page');
const MinMaxBlockPage = require('../../generated_pages/dates/min-max-block.page');
const SummaryPage = require('../../generated_pages/dates/summary.page');

describe('Date checks', function() {

  beforeEach(() => {
    openQuestionnaire('test_dates.json')
  })

  it('Given the test_dates survey is selected when dates are entered then the summary screen shows the dates entered formatted', function() {
    cy
      .get(DatesPage.dateRangeFromday()).type(1)
      .get(DatesPage.dateRangeFrommonth()).select('1')
      .get(DatesPage.dateRangeFromyear()).type(1901)

      .get(DatesPage.dateRangeToday()).type(3)
      .get(DatesPage.dateRangeTomonth()).select('5')
      .get(DatesPage.dateRangeToyear()).type(2017)

      .get(DatesPage.monthYearMonth()).select('4')
      .get(DatesPage.monthYearYear()).type(2018)

      .get(DatesPage.singleDateday()).type(4)
      .get(DatesPage.singleDatemonth()).select('1')
      .get(DatesPage.singleDateyear()).type(1999)

      .get(DatesPage.submit()).click()
      // Interstitial displaying min-max formats
      .get(MinMaxBlockPage.submit()).click()
      .url().should('contain', SummaryPage.pageName)

      // Then the summary screen shows the dates entered formatted
      .get(SummaryPage.dateRangeFromAnswer()).stripText().should('contain', '1 January 1901 to 3 May 2017')
      .get(SummaryPage.monthYearAnswer()).stripText().should('contain', 'April 2018')
      .get(SummaryPage.singleDateAnswer()).stripText().should('contain', '4 January 1999')
      .get(SummaryPage.nonMandatoryDateAnswer()).stripText().should('contain', 'No answer provided');
  });


  it('Given the test_dates survey is selected when the from date is greater than the to date then an error message is shown', function() {
    cy
      .get(DatesPage.dateRangeFromday()).type(1)
      .get(DatesPage.dateRangeFrommonth()).select('1')
      .get(DatesPage.dateRangeFromyear()).type(2016)

      .get(DatesPage.dateRangeToday()).type(1)
      .get(DatesPage.dateRangeTomonth()).select('1')
      .get(DatesPage.dateRangeToyear()).type(2015)

      .get(DatesPage.submit()).click()

      // Then an error message is shown
      .get(DatesPage.errorNumber(1)).stripText().should('contain', 'Enter a \'period to\' date later than the \'period from\' date.')

      // Then clicking error should focus on first input field
      .get(DatesPage.errorNumber(1)).click()
      .focused().should('match', DatesPage.dateRangeFromday())
  });


  it('Given the test_dates survey is selected when the from date and the to date are the same then an error message is shown', function() {
    cy
      .get(DatesPage.dateRangeFromday()).type(1)
      .get(DatesPage.dateRangeFrommonth()).select('1')
      .get(DatesPage.dateRangeFromyear()).type(2016)

      .get(DatesPage.dateRangeToday()).type(1)
      .get(DatesPage.dateRangeTomonth()).select('1')
      .get(DatesPage.dateRangeToyear()).type(2016)

      .get(DatesPage.submit()).click()

      // Then an error message is shown
      .get(DatesPage.errorNumber(1)).stripText().should('contain', 'Enter a \'period to\' date later than the \'period from\' date.');
  });


  it('Given the test_dates survey is selected when an invalid date is entered in a date range then an error message is shown', function() {
    cy
      .get(DatesPage.dateRangeFromday()).type(1)
      .get(DatesPage.dateRangeFrommonth()).select('1')
      .get(DatesPage.dateRangeFromyear()).type(2016)

      .get(DatesPage.dateRangeToday()).type(1)
      .get(DatesPage.dateRangeTomonth()).select('1')
      .get(DatesPage.dateRangeToyear()).clear()

      .get(DatesPage.submit()).click()

      // Then an error message is shown
      .get(DatesPage.errorNumber(1)).stripText().should('contain', 'Enter a valid date.');
  });


  it('Given the test_dates survey is selected when the year (month year type) is left empty then an error message is shown', function() {
    cy
      .get(DatesPage.monthYearMonth()).select('4')
      .get(DatesPage.monthYearYear()).clear()

      .get(DatesPage.submit()).click()

      // Then an error message is shown
      .get(DatesPage.errorNumber(3)).stripText().should('contain', 'Enter a valid date.');
  });


  it('Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct', function() {
    cy
      .get(DatesPage.dateRangeFromday()).type(1)
      .get(DatesPage.dateRangeFrommonth()).select('3')
      .get(DatesPage.dateRangeFromyear()).type(2016)

      .get(DatesPage.dateRangeToday()).type(3)
      .get(DatesPage.dateRangeTomonth()).select('5')
      .get(DatesPage.dateRangeToyear()).type(2017)

      .get(DatesPage.monthYearMonth()).select('4')
      .get(DatesPage.monthYearYear()).clear()

      .get(DatesPage.singleDateday()).type(4)
      .get(DatesPage.singleDatemonth()).select('1')
      .get(DatesPage.singleDateyear()).type(1999)

      .get(DatesPage.submit()).click()

      .get(DatesPage.error()).stripText().should('contain', 'Enter a valid date.')

      // Then when it is corrected, it goes to the summary page and the information is correct
      .get(DatesPage.monthYearYear()).type(2018)
      .get(DatesPage.submit()).click()
      // Interstitial displaying min-max formats
      .get(MinMaxBlockPage.submit()).click()
      .url().should('contain', SummaryPage.pageName)

      // Then the summary screen shows the dates entered formatted
      .get(SummaryPage.dateRangeFromAnswer()).stripText().should('contain', '1 March 2016 to 3 May 2017')
      .get(SummaryPage.monthYearAnswer()).stripText().should('contain', 'April 2018')
      .get(SummaryPage.singleDateAnswer()).stripText().should('contain', '4 January 1999')
      .get(SummaryPage.nonMandatoryDateAnswer()).stripText().should('contain', 'No answer provided');
  });


  it('Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct', function() {
    cy
      .get(DatesPage.nonMandatoryDateday()).type(4)
      .get(DatesPage.nonMandatoryDatemonth()).select('1')

      .get(DatesPage.submit()).click()

      // Then an error message is shown
      .get(DatesPage.errorNumber(5)).stripText().should('contain', 'Enter a valid date');
  });


  it('Given the test_dates survey is selected, when a user clicks the day label then the day subfield should gain the focus', function() {
    cy
       .get(DatesPage.singleDatedayLabel()).click()

       // Then the day subfield should gain the focus
       .focused().should('match', DatesPage.singleDateday());
  });

});


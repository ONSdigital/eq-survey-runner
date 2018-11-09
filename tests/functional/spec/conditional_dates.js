const helpers = require('../helpers');
const DatesPage = require('../generated_pages/conditional_dates/date-block.page');
const DatesConfirmationPage = require('../generated_pages/conditional_dates/date-value-test.page');
const SummaryPage = require('../generated_pages/conditional_dates/summary.page');

describe('Piped Dates', function () {

  it('Given the test_conditional_dates survey is selected when dates are entered then the summary screen shows the dates entered, formatted', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_conditional_dates.json').then(() => {
      return browser

      // When dates are entered
      .setValue(DatesPage.dateStartFromday(), 11)
      .selectByValue(DatesPage.dateStartFrommonth(), 10)
      .setValue(DatesPage.dateStartFromyear(), 2017)
      .setValue(DatesPage.dateEndToday(), 3)
      .selectByValue(DatesPage.dateEndTomonth(), 12)
      .setValue(DatesPage.dateEndToyear(), 2017)
      .click(DatesPage.submit())
      .setValue(DatesConfirmationPage.dateTest(), 1)
      .click(DatesConfirmationPage.submit())

      // Then the summary screen shows the dates entered formatted
      .getText(SummaryPage.totalRetailTurnoverQuestion()).should.eventually.contain('11 October 2017 to 3 December 2017');

    });

  });

  it('Given the test_conditional_dates survey is selected when no dates are entered then the summary screen shows the default dates in the question', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_conditional_dates.json').then(() => {
      return browser

      // When dates are entered
      .setValue(DatesPage.dateStartFromday(), '')
      .selectByValue(DatesPage.dateStartFrommonth(), '')
      .setValue(DatesPage.dateStartFromyear(), '')
      .setValue(DatesPage.dateEndToday(), '')
      .selectByValue(DatesPage.dateEndTomonth(), '')
      .setValue(DatesPage.dateEndToyear(), '')
      .click(DatesPage.submit())
      .setValue(DatesConfirmationPage.dateTest(), 2)
      .click(DatesConfirmationPage.submit())

      // Then the summary screen shows the dates entered formatted

      .getText(SummaryPage.totalRetailTurnoverQuestion()).should.eventually.contain('1 January 2017 to 1 February 2017');

    });
  });
});

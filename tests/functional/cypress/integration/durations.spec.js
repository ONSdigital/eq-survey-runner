import {openQuestionnaire} from '../helpers/helpers.js';

const DurationPage = require('../../generated_pages/durations/duration-block.page.js');
const SummaryPage = require('../../generated_pages/durations/summary.page.js');

describe('Durations', function() {

  beforeEach(function() {
    openQuestionnaire('test_durations.json');
  });

  it('Given the test_durations survey is selected when durations are entered then the summary screen shows the durations entered formatted', function() {
    cy
      .get(DurationPage.yearMonthYears()).typeForced(1)
      .get(DurationPage.yearMonthMonths()).typeForced(2)
      .get(DurationPage.mandatoryYearMonthYears()).typeForced(1)
      .get(DurationPage.mandatoryYearMonthMonths()).typeForced(2)
      .get(DurationPage.mandatoryYearYears()).typeForced(1)
      .get(DurationPage.mandatoryMonthMonths()).typeForced(1)
      .get(DurationPage.submit()).click()

      .url().should('contain', SummaryPage.pageName)
      .get(SummaryPage.yearMonthAnswer()).stripText().should('equal', '1 year 2 months')
      .get(SummaryPage.submit()).click();
  });

  it('Given the test_durations survey is selected when one of the units is 0 it is excluded from the summary', function() {
    cy
      .get(DurationPage.yearMonthYears()).typeForced(0)
      .get(DurationPage.yearMonthMonths()).typeForced(2)
      .get(DurationPage.mandatoryYearMonthYears()).typeForced(1)
      .get(DurationPage.mandatoryYearMonthMonths()).typeForced(2)
      .get(DurationPage.mandatoryYearYears()).typeForced(1)
      .get(DurationPage.mandatoryMonthMonths()).typeForced(1)
      .get(DurationPage.submit()).click()

      .url().should('contain', SummaryPage.pageName)
      .get(SummaryPage.yearMonthAnswer()).stripText().should('equal', '2 months')
      .get(SummaryPage.submit()).click();
  });

  it('Given the test_durations survey is selected when no duration is entered the summary shows no answer provided', function() {
    cy
      .get(DurationPage.mandatoryYearMonthYears()).typeForced(1)
      .get(DurationPage.mandatoryYearMonthMonths()).typeForced(2)
      .get(DurationPage.mandatoryYearYears()).typeForced(1)
      .get(DurationPage.mandatoryMonthMonths()).typeForced(1)
      .get(DurationPage.submit()).click()

      .url().should('contain', SummaryPage.pageName)
      .get(SummaryPage.yearMonthAnswer()).stripText().should('equal', 'No answer provided')
      .get(SummaryPage.submit()).click();
  });

  it('Given the test_durations survey is selected when one of the units is missing an error is shown', function() {
    cy
      .get(DurationPage.yearMonthMonths()).typeForced(2)
      .get(DurationPage.mandatoryYearMonthMonths()).typeForced(2)
      .get(DurationPage.mandatoryYearYears()).typeForced(1)
      .get(DurationPage.mandatoryMonthMonths()).typeForced(1)
      .get(DurationPage.submit()).click()

      .get(DurationPage.errorNumber(1)).stripText().should('contain', 'Enter a valid duration.')
      .get(DurationPage.errorNumber(2)).stripText().should('contain', 'Enter a valid duration.');
  });

  it('Given the test_durations survey is selected when one of the units not a number an error is shown', function() {
    cy
      .get(DurationPage.yearMonthYears()).typeForced('word')
      .get(DurationPage.yearMonthMonths()).typeForced(2)
      .get(DurationPage.mandatoryYearMonthYears()).typeForced('word')
      .get(DurationPage.mandatoryYearMonthMonths()).typeForced(2)
      .get(DurationPage.mandatoryYearYears()).typeForced(1)
      .get(DurationPage.mandatoryMonthMonths()).typeForced(1)
      .get(DurationPage.submit()).click()

      .get(DurationPage.errorNumber(1)).stripText().should('contain', 'Enter a valid duration.')
      .get(DurationPage.errorNumber(2)).stripText().should('contain', 'Enter a valid duration.');
  });

  it('Given the test_durations survey is selected when the number of months is more than 11 an error is shown', function() {
    cy
      .get(DurationPage.yearMonthYears()).typeForced(1)
      .get(DurationPage.yearMonthMonths()).typeForced(12)
      .get(DurationPage.mandatoryYearMonthYears()).typeForced(1)
      .get(DurationPage.mandatoryYearMonthMonths()).typeForced(12)
      .get(DurationPage.mandatoryYearYears()).typeForced(1)
      .get(DurationPage.mandatoryMonthMonths()).typeForced(1)
      .get(DurationPage.submit()).click()

      .get(DurationPage.errorNumber(1)).stripText().should('contain', 'Enter a valid duration.')
      .get(DurationPage.errorNumber(2)).stripText().should('contain', 'Enter a valid duration.');
  });

  it('Given the test_durations survey is selected when the mandatory duration is missing an error is shown', function() {
    cy
      .get(DurationPage.mandatoryYearYears()).typeForced(1)
      .get(DurationPage.mandatoryMonthMonths()).typeForced(1)
      .get(DurationPage.submit()).click()

      .get(DurationPage.errorNumber(1)).stripText().should('contain', 'Enter a duration to continue.');
  });
});


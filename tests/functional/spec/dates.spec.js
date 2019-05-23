const helpers = require('../helpers');
const DateRangePage = require('../generated_pages/dates/date-range-block.page');
const DateMonthYearPage = require('../generated_pages/dates/date-month-year-block.page');
const DateSinglePage = require('../generated_pages/dates/date-single-block.page');
const DateNonMandatoryPage = require('../generated_pages/dates/date-non-mandatory-block.page');
const DateYearDatePage = require('../generated_pages/dates/date-year-date-block.page');
const SummaryPage = require('../generated_pages/dates/summary.page');

describe('Date checks', function() {

  it('Given the test_dates survey is selected when dates are entered then the summary screen shows the dates entered formatted', function() {

            // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

      return browser

        // When dates are entered
        .setValue(DateRangePage.dateRangeFromday(), 1)
        .setValue(DateRangePage.dateRangeFrommonth(), 1)
        .setValue(DateRangePage.dateRangeFromyear(), 1901)

        .setValue(DateRangePage.dateRangeToday(), 3)
        .setValue(DateRangePage.dateRangeTomonth(), 5)
        .setValue(DateRangePage.dateRangeToyear(), 2017)

        .click(DateRangePage.submit())

        .setValue(DateMonthYearPage.Month(), 4)
        .setValue(DateMonthYearPage.Year(), 2018)

        .click(DateMonthYearPage.submit())

        .setValue(DateSinglePage.day(), 4)
        .setValue(DateSinglePage.month(), 1)
        .setValue(DateSinglePage.year(), 1999)

        .click(DateSinglePage.submit())

        .click(DateNonMandatoryPage.submit())

        .setValue(DateYearDatePage.Year(), 2005)

        .click(DateYearDatePage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)

        // Then the summary screen shows the dates entered formatted
        .getText(SummaryPage.dateRangeFromAnswer()).should.eventually.contain('1 January 1901 to 3 May 2017')
        .getText(SummaryPage.monthYearAnswer()).should.eventually.contain('April 2018')
        .getText(SummaryPage.singleDateAnswer()).should.eventually.contain('4 January 1999')
        .getText(SummaryPage.nonMandatoryDateAnswer()).should.eventually.contain('No answer provided')
        .getText(SummaryPage.yearDateAnswer()).should.eventually.contain('2005');
    });
  });


  it('Given the test_dates survey is selected when the from date is greater than the to date then an error message is shown', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

        return browser

          // When the from date is greater than the to date
          .setValue(DateRangePage.dateRangeFromday(), 1)
          .setValue(DateRangePage.dateRangeFrommonth(), 1)
          .setValue(DateRangePage.dateRangeFromyear(), 2016)

          .setValue(DateRangePage.dateRangeToday(), 1)
          .setValue(DateRangePage.dateRangeTomonth(), 1)
          .setValue(DateRangePage.dateRangeToyear(), 2015)

          .click(DateRangePage.submit())

          // Then an error message is shown
          .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a \'period to\' date later than the \'period from\' date.')

          // Then clicking error should focus on first input field
          .click(DateRangePage.errorNumber(1))
          .hasFocus(DateRangePage.dateRangeFromday());
    });
  });


  it('Given the test_dates survey is selected when the from date and the to date are the same then an error message is shown', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

        return browser

          // When the from date is greater than the to date
          .setValue(DateRangePage.dateRangeFromday(), 1)
          .setValue(DateRangePage.dateRangeFrommonth(), 1)
          .setValue(DateRangePage.dateRangeFromyear(), 2016)

          .setValue(DateRangePage.dateRangeToday(), 1)
          .setValue(DateRangePage.dateRangeTomonth(), 1)
          .setValue(DateRangePage.dateRangeToyear(), 2016)

          .click(DateRangePage.submit())

          // Then an error message is shown
          .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a \'period to\' date later than the \'period from\' date.');
    });
  });


  it('Given the test_dates survey is selected when an invalid date is entered in a date range then an error message is shown', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

        return browser

          // When the from date is greater than the to date
          .setValue(DateRangePage.dateRangeFromday(), 1)
          .setValue(DateRangePage.dateRangeFrommonth(), 1)
          .setValue(DateRangePage.dateRangeFromyear(), 2016)

          .setValue(DateRangePage.dateRangeToday(), 1)
          .setValue(DateRangePage.dateRangeTomonth(), 1)
          .setValue(DateRangePage.dateRangeToyear(), '')

          .click(DateRangePage.submit())

          // Then an error message is shown
          .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a valid date.');
    });
  });


  it('Given the test_dates survey is selected when the year (month year type) is left empty then an error message is shown', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

        return browser

          .url(DateMonthYearPage.url())

          // When the year (month year type) is left empty
          .setValue(DateMonthYearPage.Month(), 4)
          .setValue(DateMonthYearPage.Year(), '')

          .click(DateMonthYearPage.submit())

          // Then an error message is shown
          .getText(DateMonthYearPage.errorNumber(1)).should.eventually.contain('Enter a valid date.');
    });
  });


  it('Given the test_dates survey is selected, ' +
                  'When an error message is shown and it is corrected, ' +
                  'Then it the next question is displayed', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

      return browser

        .url(DateMonthYearPage.url())

        // When an error message is shown
        .setValue(DateMonthYearPage.Month(), 4)
        .setValue(DateMonthYearPage.Year(), '')

        .click(DateMonthYearPage.submit())

        .getText(DateMonthYearPage.error()).should.eventually.contain('Enter a valid date.')

        // Then when it is corrected, it goes to the next question
        .setValue(DateMonthYearPage.Year(), 2018)
        .click(DateMonthYearPage.submit())

        .getUrl().should.eventually.contain(DateSinglePage.url());
    });
  });


  it('Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

      return browser

        .url(DateNonMandatoryPage.url())

         // When non-madatory is partially completed
          .setValue(DateNonMandatoryPage.day(), 4)
          .setValue(DateNonMandatoryPage.month(), 1)

          .click(DateNonMandatoryPage.submit())

          // Then an error message is shown
          .getText(DateNonMandatoryPage.errorNumber(1)).should.eventually.contain('Enter a valid date');
    });
  });


  it('Given the test_dates survey is selected, when a user clicks the day label then the day subfield should gain the focus', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

      return browser

        .url(DateSinglePage.url())

         // When a user clicks the day label
         .click(DateSinglePage.dayLabel())

         // Then the day subfield should gain the focus
         .hasFocus(DateSinglePage.day());
    });
  });

});

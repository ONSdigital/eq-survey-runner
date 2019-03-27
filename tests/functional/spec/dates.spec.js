/*const helpers = require('../helpers');
const DatesPage = require('../generated_pages/dates/date-block.page');
const MinMaxBlockPage = require('../generated_pages/dates/min-max-block.page');
const SummaryPage = require('../generated_pages/dates/summary.page');

describe('Date checks', function() {

  it('Given the test_dates survey is selected when dates are entered then the summary screen shows the dates entered formatted', function() {

            // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

      return browser

        // When dates are entered
        .setValue(DatesPage.dateRangeFromday(), 1)
        .selectByValue(DatesPage.dateRangeFrommonth(), 1)
        .setValue(DatesPage.dateRangeFromyear(), 1901)

        .setValue(DatesPage.dateRangeToday(), 3)
        .selectByValue(DatesPage.dateRangeTomonth(), 5)
        .setValue(DatesPage.dateRangeToyear(), 2017)

        .selectByValue(DatesPage.monthYearMonth(), 4)
        .setValue(DatesPage.monthYearYear(), 2018)

        .setValue(DatesPage.singleDateday(), 4)
        .selectByValue(DatesPage.singleDatemonth(), 1)
        .setValue(DatesPage.singleDateyear(), 1999)

        .click(DatesPage.submit())
        // Interstitial displaying min-max formats
        .click(MinMaxBlockPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName)

        // Then the summary screen shows the dates entered formatted
        .getText(SummaryPage.dateRangeFromAnswer()).should.eventually.contain('1 January 1901 to 3 May 2017')
        .getText(SummaryPage.monthYearAnswer()).should.eventually.contain('April 2018')
        .getText(SummaryPage.singleDateAnswer()).should.eventually.contain('4 January 1999')
        .getText(SummaryPage.nonMandatoryDateAnswer()).should.eventually.contain('No answer provided');
    });
  });


  it('Given the test_dates survey is selected when the from date is greater than the to date then an error message is shown', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

        return browser

          // When the from date is greater than the to date
          .setValue(DatesPage.dateRangeFromday(), 1)
          .selectByValue(DatesPage.dateRangeFrommonth(), 1)
          .setValue(DatesPage.dateRangeFromyear(), 2016)

          .setValue(DatesPage.dateRangeToday(), 1)
          .selectByValue(DatesPage.dateRangeTomonth(), 1)
          .setValue(DatesPage.dateRangeToyear(), 2015)

          .click(DatesPage.submit())

          // Then an error message is shown
          .getText(DatesPage.errorNumber(1)).should.eventually.contain('Enter a \'period to\' date later than the \'period from\' date.')

          // Then clicking error should focus on first input field
          .click(DatesPage.errorNumber(1))
          .hasFocus(DatesPage.dateRangeFromday());
    });
  });


  it('Given the test_dates survey is selected when the from date and the to date are the same then an error message is shown', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

        return browser

          // When the from date is greater than the to date
          .setValue(DatesPage.dateRangeFromday(), 1)
          .selectByValue(DatesPage.dateRangeFrommonth(), 1)
          .setValue(DatesPage.dateRangeFromyear(), 2016)

          .setValue(DatesPage.dateRangeToday(), 1)
          .selectByValue(DatesPage.dateRangeTomonth(), 1)
          .setValue(DatesPage.dateRangeToyear(), 2016)

          .click(DatesPage.submit())

          // Then an error message is shown
          .getText(DatesPage.errorNumber(1)).should.eventually.contain('Enter a \'period to\' date later than the \'period from\' date.');
    });
  });


  it('Given the test_dates survey is selected when an invalid date is entered in a date range then an error message is shown', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

        return browser

          // When the from date is greater than the to date
          .setValue(DatesPage.dateRangeFromday(), 1)
          .selectByValue(DatesPage.dateRangeFrommonth(), 1)
          .setValue(DatesPage.dateRangeFromyear(), 2016)

          .setValue(DatesPage.dateRangeToday(), 1)
          .selectByValue(DatesPage.dateRangeTomonth(), 1)
          .setValue(DatesPage.dateRangeToyear(), '')

          .click(DatesPage.submit())

          // Then an error message is shown
          .getText(DatesPage.errorNumber(1)).should.eventually.contain('Enter a valid date.');
    });
  });


  it('Given the test_dates survey is selected when the year (month year type) is left empty then an error message is shown', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

        return browser

          // When the year (month year type) is left empty
          .selectByValue(DatesPage.monthYearMonth(), 4)
          .setValue(DatesPage.monthYearYear(), '')

          .click(DatesPage.submit())

          // Then an error message is shown
          .getText(DatesPage.errorNumber(3)).should.eventually.contain('Enter a valid date.');
    });
  });


  it('Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

      return browser

        // When an error message is shown
        .setValue(DatesPage.dateRangeFromday(), 1)
        .selectByValue(DatesPage.dateRangeFrommonth(), 3)
        .setValue(DatesPage.dateRangeFromyear(), 2016)

        .setValue(DatesPage.dateRangeToday(), 3)
        .selectByValue(DatesPage.dateRangeTomonth(), 5)
        .setValue(DatesPage.dateRangeToyear(), 2017)

        .selectByValue(DatesPage.monthYearMonth(), 4)
        .setValue(DatesPage.monthYearYear(), '')

        .setValue(DatesPage.singleDateday(), 4)
        .selectByValue(DatesPage.singleDatemonth(), 1)
        .setValue(DatesPage.singleDateyear(), 1999)

        .click(DatesPage.submit())

        .getText(DatesPage.error()).should.eventually.contain('Enter a valid date.')

        // Then when it is corrected, it goes to the summary page and the information is correct
        .setValue(DatesPage.monthYearYear(), 2018)
        .click(DatesPage.submit())
        // Interstitial displaying min-max formats
        .click(MinMaxBlockPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName)

        // Then the summary screen shows the dates entered formatted
        .getText(SummaryPage.dateRangeFromAnswer()).should.eventually.contain('1 March 2016 to 3 May 2017')
        .getText(SummaryPage.monthYearAnswer()).should.eventually.contain('April 2018')
        .getText(SummaryPage.singleDateAnswer()).should.eventually.contain('4 January 1999')
        .getText(SummaryPage.nonMandatoryDateAnswer()).should.eventually.contain('No answer provided');
    });
  });


  it('Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

      return browser

         // When non-madatory is partially completed
          .setValue(DatesPage.nonMandatoryDateday(), 4)
          .selectByValue(DatesPage.nonMandatoryDatemonth(), 1)

          .click(DatesPage.submit())

          // Then an error message is shown
          .getText(DatesPage.errorNumber(5)).should.eventually.contain('Enter a valid date');
    });
  });


  it('Given the test_dates survey is selected, when a user clicks the day label then the day subfield should gain the focus', function() {

    // Given the test_dates survey is selected
    return helpers.openQuestionnaire('test_dates.json').then(() => {

      return browser

         // When a user clicks the day label
         .click(DatesPage.singleDatedayLabel())

         // Then the day subfield should gain the focus
         .hasFocus(DatesPage.singleDateday());
    });
  });

});
*/

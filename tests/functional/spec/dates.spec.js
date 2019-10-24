const helpers = require('../helpers');
const DateRangePage = require('../generated_pages/dates/date-range-block.page');
const DateMonthYearPage = require('../generated_pages/dates/date-month-year-block.page');
const DateSinglePage = require('../generated_pages/dates/date-single-block.page');
const DateNonMandatoryPage = require('../generated_pages/dates/date-non-mandatory-block.page');
const DateYearDatePage = require('../generated_pages/dates/date-year-date-block.page');
const SummaryPage = require('../generated_pages/dates/summary.page');

describe('Date checks', function() {
  let browser;

  beforeEach('Load the survey', function () {
    helpers.openQuestionnaire('test_dates.json').then(openBrowser => browser = openBrowser);
  });

  it('Given the test_dates survey is selected when dates are entered then the summary screen shows the dates entered formatted', function() {
    // When dates are entered
    $(DateRangePage.dateRangeFromday()).setValue(1);
    $(DateRangePage.dateRangeFrommonth()).setValue(1);
    $(DateRangePage.dateRangeFromyear()).setValue(1901);

    $(DateRangePage.dateRangeToday()).setValue(3);
    $(DateRangePage.dateRangeTomonth()).setValue(5);
    $(DateRangePage.dateRangeToyear()).setValue(2017);

    $(DateRangePage.submit()).click();

    $(DateMonthYearPage.Month()).setValue(4);
    $(DateMonthYearPage.Year()).setValue(2018);

    $(DateMonthYearPage.submit()).click();

    $(DateSinglePage.day()).setValue(4);
    $(DateSinglePage.month()).setValue(1);
    $(DateSinglePage.year()).setValue(1999);

    $(DateSinglePage.submit()).click();

    $(DateNonMandatoryPage.submit()).click();

    $(DateYearDatePage.Year()).setValue(2005);

    $(DateYearDatePage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);

    // Then the summary screen shows the dates entered formatted
    expect($(SummaryPage.dateRangeFromAnswer()).getText()).to.contain('1 January 1901 to 3 May 2017');
    expect($(SummaryPage.monthYearAnswer()).getText()).to.contain('April 2018');
    expect($(SummaryPage.singleDateAnswer()).getText()).to.contain('4 January 1999');
    expect($(SummaryPage.nonMandatoryDateAnswer()).getText()).to.contain('No answer provided');
    expect($(SummaryPage.yearDateAnswer()).getText()).to.contain('2005');
  });


  it('Given the test_dates survey is selected when the from date is greater than the to date then an error message is shown', function() {
    // When the from date is greater than the to date
    $(DateRangePage.dateRangeFromday()).setValue(1);
    $(DateRangePage.dateRangeFrommonth()).setValue(1);
    $(DateRangePage.dateRangeFromyear()).setValue(2016);

    $(DateRangePage.dateRangeToday()).setValue(1);
    $(DateRangePage.dateRangeTomonth()).setValue(1);
    $(DateRangePage.dateRangeToyear()).setValue(2015);

    $(DateRangePage.submit()).click();

    // Then an error message is shown
    expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a \'period to\' date later than the \'period from\' date.');

    // Then clicking error should focus on first input field
    $(DateRangePage.errorNumber(1)).click();
    expect($(DateRangePage.dateRangeFromday()).isFocused()).to.be.true;
  });


  it('Given the test_dates survey is selected when the from date and the to date are the same then an error message is shown', function() {
    // When the from date is greater than the to date
    $(DateRangePage.dateRangeFromday()).setValue(1);
    $(DateRangePage.dateRangeFrommonth()).setValue(1);
    $(DateRangePage.dateRangeFromyear()).setValue(2016);

    $(DateRangePage.dateRangeToday()).setValue(1);
    $(DateRangePage.dateRangeTomonth()).setValue(1);
    $(DateRangePage.dateRangeToyear()).setValue(2016);

    $(DateRangePage.submit()).click();

    // Then an error message is shown
    expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a \'period to\' date later than the \'period from\' date.');
  });


  it('Given the test_dates survey is selected when an invalid date is entered in a date range then an error message is shown', function() {
    // When the from date is greater than the to date
    $(DateRangePage.dateRangeFromday()).setValue(1);
    $(DateRangePage.dateRangeFrommonth()).setValue(1);
    $(DateRangePage.dateRangeFromyear()).setValue(2016);

    $(DateRangePage.dateRangeToday()).setValue(1);
    $(DateRangePage.dateRangeTomonth()).setValue(1);
    $(DateRangePage.dateRangeToyear()).setValue('');

    $(DateRangePage.submit()).click();

    // Then an error message is shown
    expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a valid date.');
  });


  it('Given the test_dates survey is selected when the year (month year type) is left empty then an error message is shown', function() {
    $(DateRangePage.dateRangeFromday()).setValue(1);
    $(DateRangePage.dateRangeFrommonth()).setValue(1);
    $(DateRangePage.dateRangeFromyear()).setValue(2016);
    $(DateRangePage.dateRangeToday()).setValue(1);
    $(DateRangePage.dateRangeTomonth()).setValue(1);
    $(DateRangePage.dateRangeToyear()).setValue(2017);
    $(DateRangePage.submit()).click();

    // When the year (month year type) is left empty
    $(DateMonthYearPage.Month()).setValue(4);
    $(DateMonthYearPage.Year()).setValue('');

    $(DateMonthYearPage.submit()).click();

    // Then an error message is shown
    expect($(DateMonthYearPage.errorNumber(1)).getText()).to.contain('Enter a valid date.');
  });


  it('Given the test_dates survey is selected, ' +
  'When an error message is shown and it is corrected, ' +
  'Then the next question is displayed', function() {
    $(DateRangePage.dateRangeFromday()).setValue(1);
    $(DateRangePage.dateRangeFrommonth()).setValue(1);
    $(DateRangePage.dateRangeFromyear()).setValue(2016);
    $(DateRangePage.dateRangeToday()).setValue(1);
    $(DateRangePage.dateRangeTomonth()).setValue(1);
    $(DateRangePage.dateRangeToyear()).setValue(2017);
    $(DateRangePage.submit()).click();

    // When an error message is shown
    $(DateMonthYearPage.Month()).setValue(4);
    $(DateMonthYearPage.Year()).setValue('');
    $(DateMonthYearPage.submit()).click();

    expect($(DateMonthYearPage.error()).getText()).to.contain('Enter a valid date.');

    // Then when it is corrected, it goes to the next question
    $(DateMonthYearPage.Year()).setValue(2018);
    $(DateMonthYearPage.submit()).click();

    expect(browser.getUrl()).to.contain(DateSinglePage.url());
  });


  it('Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct', function() {
    $(DateRangePage.dateRangeFromday()).setValue(1);
    $(DateRangePage.dateRangeFrommonth()).setValue(1);
    $(DateRangePage.dateRangeFromyear()).setValue(2016);
    $(DateRangePage.dateRangeToday()).setValue(1);
    $(DateRangePage.dateRangeTomonth()).setValue(1);
    $(DateRangePage.dateRangeToyear()).setValue(2017);
    $(DateRangePage.submit()).click();

    $(DateMonthYearPage.Month()).setValue(1);
    $(DateMonthYearPage.Year()).setValue(2016);
    $(DateMonthYearPage.submit()).click();

    $(DateSinglePage.day()).setValue(1);
    $(DateSinglePage.month()).setValue(1);
    $(DateSinglePage.year()).setValue(2016);
    $(DateMonthYearPage.submit()).click();

    // When non-mandatory is partially completed
    $(DateNonMandatoryPage.day()).setValue(4);
    $(DateNonMandatoryPage.month()).setValue(1);
    $(DateNonMandatoryPage.submit()).click();

    // Then an error message is shown
    expect($(DateNonMandatoryPage.errorNumber(1)).getText()).to.contain('Enter a valid date');
  });


  it('Given the test_dates survey is selected, when a user clicks the day label then the day subfield should gain the focus', function() {
    $(DateRangePage.dateRangeFromday()).setValue(1);
    $(DateRangePage.dateRangeFrommonth()).setValue(1);
    $(DateRangePage.dateRangeFromyear()).setValue(2016);
    $(DateRangePage.dateRangeToday()).setValue(1);
    $(DateRangePage.dateRangeTomonth()).setValue(1);
    $(DateRangePage.dateRangeToyear()).setValue(2017);
    $(DateRangePage.submit()).click();

    $(DateMonthYearPage.Month()).setValue(1);
    $(DateMonthYearPage.Year()).setValue(2016);
    $(DateMonthYearPage.submit()).click();

    // When a user clicks the day label
    $(DateSinglePage.dayLabel()).click();

    // Then the day subfield should gain the focus
    expect($(DateSinglePage.day()).isFocused()).to.be.true;
  });
});

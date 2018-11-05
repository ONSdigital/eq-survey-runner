const helpers = require('../helpers');

const DurationPage = require('../generated_pages/durations/duration-block.page.js');
const SummaryPage = require('../generated_pages/durations/summary.page.js');

describe('Durations', function() {

  it('Given the test_durations survey is selected when durations are entered then the summary screen shows the durations entered formatted', function() {

    return helpers.openQuestionnaire('test_durations.json').then(() => {

      return browser
        .setValue(DurationPage.yearMonthYears(), 1)
        .setValue(DurationPage.yearMonthMonths(), 2)
        .setValue(DurationPage.mandatoryYearMonthYears(), 1)
        .setValue(DurationPage.mandatoryYearMonthMonths(), 2)
        .setValue(DurationPage.mandatoryYearYears(), 1)
        .setValue(DurationPage.mandatoryMonthMonths(), 1)
        .click(DurationPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.yearMonthAnswer()).should.eventually.equal('1 year 2 months')
        .click(SummaryPage.submit());
    });
  });

  it('Given the test_durations survey is selected when one of the units is 0 it is excluded from the summary', function() {

    return helpers.openQuestionnaire('test_durations.json').then(() => {

      return browser
        .setValue(DurationPage.yearMonthYears(), 0)
        .setValue(DurationPage.yearMonthMonths(), 2)
        .setValue(DurationPage.mandatoryYearMonthYears(), 1)
        .setValue(DurationPage.mandatoryYearMonthMonths(), 2)
        .setValue(DurationPage.mandatoryYearYears(), 1)
        .setValue(DurationPage.mandatoryMonthMonths(), 1)
        .click(DurationPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.yearMonthAnswer()).should.eventually.equal('2 months')
        .click(SummaryPage.submit());
    });
  });

  it('Given the test_durations survey is selected when no duration is entered the summary shows no answer provided', function() {

    return helpers.openQuestionnaire('test_durations.json').then(() => {

      return browser
        .setValue(DurationPage.mandatoryYearMonthYears(), 1)
        .setValue(DurationPage.mandatoryYearMonthMonths(), 2)
        .setValue(DurationPage.mandatoryYearYears(), 1)
        .setValue(DurationPage.mandatoryMonthMonths(), 1)
        .click(DurationPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.yearMonthAnswer()).should.eventually.equal('No answer provided')
        .click(SummaryPage.submit());
    });
  });

  it('Given the test_durations survey is selected when one of the units is missing an error is shown', function() {

    return helpers.openQuestionnaire('test_durations.json').then(() => {

      return browser
        .setValue(DurationPage.yearMonthMonths(), 2)
        .setValue(DurationPage.mandatoryYearMonthMonths(), 2)
        .setValue(DurationPage.mandatoryYearYears(), 1)
        .setValue(DurationPage.mandatoryMonthMonths(), 1)
        .click(DurationPage.submit())

        .getText(DurationPage.errorNumber(1)).should.eventually.contain('Enter a valid duration.')
        .getText(DurationPage.errorNumber(2)).should.eventually.contain('Enter a valid duration.');
    });
  });

  it('Given the test_durations survey is selected when one of the units not a number an error is shown', function() {

    return helpers.openQuestionnaire('test_durations.json').then(() => {

      return browser
        .setValue(DurationPage.yearMonthYears(), 'word')
        .setValue(DurationPage.yearMonthMonths(), 2)
        .setValue(DurationPage.mandatoryYearMonthYears(), 'word')
        .setValue(DurationPage.mandatoryYearMonthMonths(), 2)
        .setValue(DurationPage.mandatoryYearYears(), 1)
        .setValue(DurationPage.mandatoryMonthMonths(), 1)
        .click(DurationPage.submit())

        .getText(DurationPage.errorNumber(1)).should.eventually.contain('Enter a valid duration.')
        .getText(DurationPage.errorNumber(2)).should.eventually.contain('Enter a valid duration.');
    });
  });

  it('Given the test_durations survey is selected when the number of months is more than 11 an error is shown', function() {

    return helpers.openQuestionnaire('test_durations.json').then(() => {

      return browser
        .setValue(DurationPage.yearMonthYears(), 1)
        .setValue(DurationPage.yearMonthMonths(), 12)
        .setValue(DurationPage.mandatoryYearMonthYears(), 1)
        .setValue(DurationPage.mandatoryYearMonthMonths(), 12)
        .setValue(DurationPage.mandatoryYearYears(), 1)
        .setValue(DurationPage.mandatoryMonthMonths(), 1)
        .click(DurationPage.submit())

        .getText(DurationPage.errorNumber(1)).should.eventually.contain('Enter a valid duration.')
        .getText(DurationPage.errorNumber(2)).should.eventually.contain('Enter a valid duration.');
    });
  });

  it('Given the test_durations survey is selected when the mandatory duration is missing an error is shown', function() {

    return helpers.openQuestionnaire('test_durations.json').then(() => {

      return browser
        .setValue(DurationPage.mandatoryYearYears(), 1)
        .setValue(DurationPage.mandatoryMonthMonths(), 1)
        .click(DurationPage.submit())

        .getText(DurationPage.errorNumber(1)).should.eventually.contain('Enter a duration to continue.');
    });
  });
});


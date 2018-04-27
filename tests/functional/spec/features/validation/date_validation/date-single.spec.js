const helpers = require('../../../../helpers');

describe('Feature: Validation for single date periods', function() {
  var DatePage = require('../../../../pages/features/validation/date-validation/date-single/date-block.page');
  var DatePeriodPage = require('../../../../pages/features/validation/date-validation/date-single/date-range-block.page');
  var SummaryPage = require('../../../../pages/features/validation/date-validation/date-single/summary.page');

  beforeEach(function() {
     return helpers.openQuestionnaire('test_date_validation_single.json')
      .then(completeFirstDatePage)
      .then(() => {
      });
  });

  describe('Given I enter a date before the minimum offset meta date', function() {
    it('When I continue, Then I should see a period validation error', function() {
      return browser
       .setValue(DatePeriodPage.dateRangeFromday(), 13)
       .selectByValue(DatePeriodPage.dateRangeFrommonth(), 2)
       .setValue(DatePeriodPage.dateRangeFromyear(), 2016)
       .click(DatePeriodPage.submit())

       .setValue(DatePeriodPage.dateRangeToday(), 3)
       .selectByValue(DatePeriodPage.dateRangeTomonth(), 3)
       .setValue(DatePeriodPage.dateRangeToyear(), 2018)
       .click(DatePeriodPage.submit())
       .getText(DatePeriodPage.errorNumber(1)).should.eventually.contain('Enter a date after 12 December 2016.');
     });
  });

  describe('Given I enter a date after the maximum offset value date', function() {
    it('When I continue, Then I should see a period validation error', function() {
      return browser
       .setValue(DatePeriodPage.dateRangeFromday(), 13)
       .selectByValue(DatePeriodPage.dateRangeFrommonth(), 7)
       .setValue(DatePeriodPage.dateRangeFromyear(), 2017)
       .click(DatePeriodPage.submit())

       .setValue(DatePeriodPage.dateRangeToday(), 3)
       .selectByValue(DatePeriodPage.dateRangeTomonth(), 3)
       .setValue(DatePeriodPage.dateRangeToyear(), 2018)
       .click(DatePeriodPage.submit())
       .getText(DatePeriodPage.errorNumber(1)).should.eventually.contain('Enter a date before 2 July 2017.');
     });
  });

  describe('Given I enter a date before the minimum offset answer id date', function() {
    it('When I continue, Then I should see a period validation error', function() {
      return browser
       .setValue(DatePeriodPage.dateRangeFromday(), 13)
       .selectByValue(DatePeriodPage.dateRangeFrommonth(), 11)
       .setValue(DatePeriodPage.dateRangeFromyear(), 2016)
       .click(DatePeriodPage.submit())

       .setValue(DatePeriodPage.dateRangeToday(), 13)
       .selectByValue(DatePeriodPage.dateRangeTomonth(), 1)
       .setValue(DatePeriodPage.dateRangeToyear(), 2018)
       .click(DatePeriodPage.submit())
       .getText(DatePeriodPage.errorNumber(2)).should.eventually.contain('Enter a date after 10 February 2018.');
     });
  });

  describe('Given I enter a date in between the minimum offset meta date and the maximum offset value date', function() {
    it('When I continue, Then I should be able to reach the summary', function() {
      return browser
       .setValue(DatePeriodPage.dateRangeFromday(), 13)
       .selectByValue(DatePeriodPage.dateRangeFrommonth(), 12)
       .setValue(DatePeriodPage.dateRangeFromyear(), 2016)
       .click(DatePeriodPage.submit())

       .setValue(DatePeriodPage.dateRangeToday(), 11)
       .selectByValue(DatePeriodPage.dateRangeTomonth(), 2)
       .setValue(DatePeriodPage.dateRangeToyear(), 2018)
       .click(DatePeriodPage.submit())
       .getUrl().should.eventually.contain(SummaryPage.pageName);
     });
  });

  function completeFirstDatePage() {
    return browser
     .setValue(DatePage.day(), 1)
     .selectByValue(DatePage.month(), 1)
     .setValue(DatePage.year(), 2018)
     .click(DatePage.submit());
  }

});

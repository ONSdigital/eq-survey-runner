const helpers = require('../../../../helpers');

describe('Feature: Question level validation for date ranges', function() {
  var DateRangePage = require('../../../../generated_pages/date_validation_range/date-range-block.page');
  var SummaryPage = require('../../../../generated_pages/date_validation_range/summary.page');

  beforeEach(function() {
        return helpers.openQuestionnaire('test_date_validation_range.json');
  });

  describe('Period Validation', function () {
    describe('Given I enter a date period greater than the max period limit', function() {
      it('When I continue, Then I should see a period validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromday(), 1)
         .setValue(DateRangePage.dateRangeFrommonth(), 1)
         .setValue(DateRangePage.dateRangeFromyear(), 2018)

         .setValue(DateRangePage.dateRangeToday(), 3)
         .setValue(DateRangePage.dateRangeTomonth(), 3)
         .setValue(DateRangePage.dateRangeToyear(), 2018)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a reporting period less than or equal to 1 month, 20 days.');
       });
    });

    describe('Given I enter a date period less than the min period limit', function() {
      it('When I continue, Then I should see a period validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromday(), 1)
         .setValue(DateRangePage.dateRangeFrommonth(), 1)
         .setValue(DateRangePage.dateRangeFromyear(), 2018)

         .setValue(DateRangePage.dateRangeToday(), 3)
         .setValue(DateRangePage.dateRangeTomonth(), 1)
         .setValue(DateRangePage.dateRangeToyear(), 2018)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a reporting period greater than or equal to 23 days.');
       });
    });

    describe('Given I enter a date period within the set period limits', function() {
      it('When I continue, Then I should be able to reach the summary', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromday(), 1)
         .setValue(DateRangePage.dateRangeFrommonth(), 1)
         .setValue(DateRangePage.dateRangeFromyear(), 2018)

         .setValue(DateRangePage.dateRangeToday(), 3)
         .setValue(DateRangePage.dateRangeTomonth(), 2)
         .setValue(DateRangePage.dateRangeToyear(), 2018)
         .click(DateRangePage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
       });
    });
  });

  describe('Date Range Validation', function () {
    describe('Given I enter a "to date" which is earlier than the "from date"', function() {
      it('When I continue, Then I should see a validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromday(), 1)
         .setValue(DateRangePage.dateRangeFrommonth(), 2)
         .setValue(DateRangePage.dateRangeFromyear(), 2018)

         .setValue(DateRangePage.dateRangeToday(), 3)
         .setValue(DateRangePage.dateRangeTomonth(), 1)
         .setValue(DateRangePage.dateRangeToyear(), 2018)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a \'period to\' date later than the \'period from\' date.');
       });
    });

    describe('Given I enter matching dates for the "from" and "to" dates', function() {
      it('When I continue, Then I should see a validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromday(), 1)
         .setValue(DateRangePage.dateRangeFrommonth(), 1)
         .setValue(DateRangePage.dateRangeFromyear(), 2018)

         .setValue(DateRangePage.dateRangeToday(), 1)
         .setValue(DateRangePage.dateRangeTomonth(), 1)
         .setValue(DateRangePage.dateRangeToyear(), 2018)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a \'period to\' date later than the \'period from\' date.');
       });
    });

    describe('Given I enter a valid date range', function() {
      it('When I continue, Then I should be able to reach the summary', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromday(), 1)
         .setValue(DateRangePage.dateRangeFrommonth(), 1)
         .setValue(DateRangePage.dateRangeFromyear(), 2018)

         .setValue(DateRangePage.dateRangeToday(), 3)
         .setValue(DateRangePage.dateRangeTomonth(), 2)
         .setValue(DateRangePage.dateRangeToyear(), 2018)
         .click(DateRangePage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
       });
    });
  });
});

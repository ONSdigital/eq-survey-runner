const helpers = require('../../../../helpers');
const DateRangePage = require('../../../../pages/features/validation/date-validation/date-combined-mm-yyyy/date-range-block.page');
var SummaryPage = require('../../../../pages/features/validation/date-validation/date-combined-mm-yyyy/summary.page');

describe('Feature: Combined question level and single validation for MM-YYYY dates', function() {

  before(function() {
    return helpers.openQuestionnaire('test_date_validation_mm_yyyy_combined.json');
  });

  describe('Period Validation', function () {
    describe('Given I enter dates', function() {

      it('When I enter a single dates that are too early/late, Then I should see a single validation errors', function() {
        return browser
         .selectByValue(DateRangePage.dateRangeFrommonth(), 10)
         .setValue(DateRangePage.dateRangeFromyear(), 2016)

         .selectByValue(DateRangePage.dateRangeTomonth(), 6)
         .setValue(DateRangePage.dateRangeToyear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a date after November 2016.')
         .getText(DateRangePage.errorNumber(2)).should.eventually.contain('Enter a date before June 2017.');
      });

      it('When I enter a range too large, Then I should see a range validation error', function() {
        return browser
         .selectByValue(DateRangePage.dateRangeFrommonth(), 12)
         .setValue(DateRangePage.dateRangeFromyear(), 2016)

         .selectByValue(DateRangePage.dateRangeTomonth(), 5)
         .setValue(DateRangePage.dateRangeToyear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a reporting period less than or equal to 3 months.');
      });

      it('When I enter a range too small, Then I should see a range validation error', function() {
        return browser
         .selectByValue(DateRangePage.dateRangeFrommonth(), 12)
         .setValue(DateRangePage.dateRangeFromyear(), 2016)

         .selectByValue(DateRangePage.dateRangeTomonth(), 1)
         .setValue(DateRangePage.dateRangeToyear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a reporting period greater than or equal to 2 months.');
      });

      it('When I enter valid dates, Then I should see the summary page', function() {
        return browser
         .selectByValue(DateRangePage.dateRangeFrommonth(), 1)
         .setValue(DateRangePage.dateRangeFromyear(), 2017)

         // Min range
         .selectByValue(DateRangePage.dateRangeTomonth(), 3)
         .setValue(DateRangePage.dateRangeToyear(), 2017)
         .click(DateRangePage.submit())
         .getText(SummaryPage.dateRange()).should.eventually.contain('January 2017 to March 2017')

         // Max range
         .click(SummaryPage.dateRangeEdit())
         .selectByValue(DateRangePage.dateRangeTomonth(), 4)
         .setValue(DateRangePage.dateRangeToyear(), 2017)
         .click(DateRangePage.submit())
         .getText(SummaryPage.dateRange()).should.eventually.contain('January 2017 to April 2017');
      });

    });

  });
});

const helpers = require('../../../../helpers');
const DateRangePage = require('../../../../generated_pages/date_validation_combined/date-range-block.page');
var SummaryPage = require('../../../../generated_pages/date_validation_combined/summary.page');

describe('Feature: Combined question level and single validation for dates', function() {

  before(function() {
    return helpers.openQuestionnaire('test_date_validation_combined.json');
  });

  describe('Period Validation', function () {
    describe('Given I enter dates', function() {

      it('When I enter a single dates that are too early/late, Then I should see a single validation errors', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromday(), 12)
         .setValue(DateRangePage.dateRangeFrommonth(), 12)
         .setValue(DateRangePage.dateRangeFromyear(), 2016)

         .setValue(DateRangePage.dateRangeToday(), 22)
         .setValue(DateRangePage.dateRangeTomonth(), 2)
         .setValue(DateRangePage.dateRangeToyear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a date after 12 December 2016.')
         .getText(DateRangePage.errorNumber(2)).should.eventually.contain('Enter a date before 22 February 2017.');
      });

      it('When I enter a range too large, Then I should see a range validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromday(), 13)
         .setValue(DateRangePage.dateRangeFrommonth(), 12)
         .setValue(DateRangePage.dateRangeFromyear(), 2016)

         .setValue(DateRangePage.dateRangeToday(), 21)
         .setValue(DateRangePage.dateRangeTomonth(), 2)
         .setValue(DateRangePage.dateRangeToyear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a reporting period less than or equal to 50 days.');
      });

      it('When I enter a range too small, Then I should see a range validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromday(), 1)
         .setValue(DateRangePage.dateRangeFrommonth(), 1)
         .setValue(DateRangePage.dateRangeFromyear(), 2017)

         .setValue(DateRangePage.dateRangeToday(), 10)
         .setValue(DateRangePage.dateRangeTomonth(), 1)
         .setValue(DateRangePage.dateRangeToyear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a reporting period greater than or equal to 10 days.');
      });

      it('When I enter valid dates, Then I should see the summary page', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromday(), 1)
         .setValue(DateRangePage.dateRangeFrommonth(), 1)
         .setValue(DateRangePage.dateRangeFromyear(), 2017)

         // Min range
         .setValue(DateRangePage.dateRangeToday(), 11)
         .setValue(DateRangePage.dateRangeTomonth(), 1)
         .setValue(DateRangePage.dateRangeToyear(), 2017)
         .click(DateRangePage.submit())
         .getText(SummaryPage.dateRangeFrom()).should.eventually.contain('1 January 2017 to 11 January 2017')

         // Max range
         .click(SummaryPage.dateRangeFromEdit())
         .setValue(DateRangePage.dateRangeToday(), 20)
         .setValue(DateRangePage.dateRangeTomonth(), 2)
         .setValue(DateRangePage.dateRangeToyear(), 2017)
         .click(DateRangePage.submit())
         .getText(SummaryPage.dateRangeFrom()).should.eventually.contain('1 January 2017 to 20 February 2017');
      });

    });

  });
});

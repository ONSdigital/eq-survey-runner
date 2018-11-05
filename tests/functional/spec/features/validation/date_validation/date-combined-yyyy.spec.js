const helpers = require('../../../../helpers');
const DateRangePage = require('../../../../generated_pages/date_validation_yyyy_combined/date-range-block.page');
var SummaryPage = require('../../../../generated_pages/date_validation_yyyy_combined/summary.page');

describe('Feature: Combined question level and single validation for MM-YYYY dates', function() {

  before(function() {
    return helpers.openQuestionnaire('test_date_validation_yyyy_combined.json');
  });

  describe('Period Validation', function () {
    describe('Given I enter dates', function() {

      it('When I enter a single dates that are too early/late, Then I should see a single validation errors', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromYear(), 2015)
         .setValue(DateRangePage.dateRangeToYear(), 2021)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a date after 2015.')
         .getText(DateRangePage.errorNumber(2)).should.eventually.contain('Enter a date before 2021.');
      });

      it('When I enter a range too large, Then I should see a range validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromYear(), 2016)
         .setValue(DateRangePage.dateRangeToYear(), 2020)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a reporting period less than or equal to 3 years.');
      });

      it('When I enter a range too small, Then I should see a range validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromYear(), 2016)
         .setValue(DateRangePage.dateRangeToYear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a reporting period greater than or equal to 2 years.');
      });

      it('When I enter an invalid year, Then I should see a single validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromYear(), 2016)
         .setValue(DateRangePage.dateRangeToYear(), 20167)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a valid date.')
         .isExisting(DateRangePage.errorNumber(2)).should.eventually.be.false;
      });

      it('When I enter valid dates, Then I should see the summary page', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromYear(), 2016)
         // Min range
         .setValue(DateRangePage.dateRangeToYear(), 2018)
         .click(DateRangePage.submit())
         .getText(SummaryPage.dateRangeFrom()).should.eventually.contain('2016 to 2018')

         // Max range
         .click(SummaryPage.dateRangeFromEdit())
         .setValue(DateRangePage.dateRangeToYear(), 2019)
         .click(DateRangePage.submit())
         .getText(SummaryPage.dateRangeFrom()).should.eventually.contain('2016 to 2019');
      });

    });

  });
});

const helpers = require('../../../../helpers');
const DateRangePage = require('../../../../generated_pages/date_validation_mm_yyyy_combined/date-range-block.page');
const SummaryPage = require('../../../../generated_pages/date_validation_mm_yyyy_combined/summary.page');

describe('Feature: Combined question level and single validation for MM-YYYY dates', function() {

  before(function() {
    return helpers.openQuestionnaire('test_date_validation_mm_yyyy_combined.json');
  });

  describe('Period Validation', function () {
    describe('Given I enter dates', function() {

      it('When I enter a month but no year, Then I should see only a single invalid date error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromYear(), 2018)

         .setValue(DateRangePage.dateRangeToMonth(), 4)
         .setValue(DateRangePage.dateRangeToYear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a valid date')
         .isExisting(DateRangePage.errorNumber(2)).should.eventually.be.false;
      });

      it('When I enter a year but no month, Then I should see only a single invalid date error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromMonth(), 10)
         .setValue(DateRangePage.dateRangeFromYear(), '')

         .setValue(DateRangePage.dateRangeToMonth(), 4)
         .setValue(DateRangePage.dateRangeToYear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a valid date')
         .isExisting(DateRangePage.errorNumber(2)).should.eventually.be.false;
      });

      it('When I enter a year of 0, Then I should see only a single invalid date error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromMonth(), 10)
         .setValue(DateRangePage.dateRangeFromYear(), 0)

         .setValue(DateRangePage.dateRangeToMonth(), 4)
         .setValue(DateRangePage.dateRangeToYear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a valid date')
         .isExisting(DateRangePage.errorNumber(2)).should.eventually.be.false;
      });

      it('When I enter a year that contains more than 4 characters, Then I should see only a single invalid date error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromMonth(), 10)
         .setValue(DateRangePage.dateRangeFromYear(), 10001)

         .setValue(DateRangePage.dateRangeToMonth(), 4)
         .setValue(DateRangePage.dateRangeToYear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a valid date')
         .isExisting(DateRangePage.errorNumber(2)).should.eventually.be.false;
      });

      it('When I enter a single dates that are too early/late, Then I should see a single validation errors', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromMonth(), 10)
         .setValue(DateRangePage.dateRangeFromYear(), 2016)

         .setValue(DateRangePage.dateRangeToMonth(), 6)
         .setValue(DateRangePage.dateRangeToYear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a date after November 2016.')
         .getText(DateRangePage.errorNumber(2)).should.eventually.contain('Enter a date before June 2017.');
      });

      it('When I enter a range too large, Then I should see a range validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromMonth(), 12)
         .setValue(DateRangePage.dateRangeFromYear(), 2016)

         .setValue(DateRangePage.dateRangeToMonth(), 5)
         .setValue(DateRangePage.dateRangeToYear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a reporting period less than or equal to 3 months.');
      });

      it('When I enter a range too small, Then I should see a range validation error', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromMonth(), 12)
         .setValue(DateRangePage.dateRangeFromYear(), 2016)

         .setValue(DateRangePage.dateRangeToMonth(), 1)
         .setValue(DateRangePage.dateRangeToYear(), 2017)
         .click(DateRangePage.submit())
         .getText(DateRangePage.errorNumber(1)).should.eventually.contain('Enter a reporting period greater than or equal to 2 months.');
      });

      it('When I enter valid dates, Then I should see the summary page', function() {
        return browser
         .setValue(DateRangePage.dateRangeFromMonth(), 1)
         .setValue(DateRangePage.dateRangeFromYear(), 2017)

         // Min range
         .setValue(DateRangePage.dateRangeToMonth(), 3)
         .setValue(DateRangePage.dateRangeToYear(), 2017)
         .click(DateRangePage.submit())
         .getText(SummaryPage.dateRangeFrom()).should.eventually.contain('January 2017 to March 2017')

         // Max range
         .click(SummaryPage.dateRangeFromEdit())
         .setValue(DateRangePage.dateRangeToMonth(), 4)
         .setValue(DateRangePage.dateRangeToYear(), 2017)
         .click(DateRangePage.submit())
         .getText(SummaryPage.dateRangeFrom()).should.eventually.contain('January 2017 to April 2017');
      });

    });

  });
});

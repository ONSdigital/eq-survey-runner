const helpers = require('../../../../helpers');
const DateRangePage = require('../../../../generated_pages/date_validation_mm_yyyy_combined/date-range-block.page');
const SummaryPage = require('../../../../generated_pages/date_validation_mm_yyyy_combined/summary.page');

describe('Feature: Combined question level and single validation for MM-YYYY dates', function() {
  let browser;

  before(function() {
    browser = helpers.openQuestionnaire('test_date_validation_mm_yyyy_combined.json');
  });

  describe('Period Validation', function () {
    describe('Given I enter dates', function() {

      it('When I enter a month but no year, Then I should see only a single invalid date error', function() {
         $(DateRangePage.dateRangeFromYear()).setValue(2018);

         $(DateRangePage.dateRangeToMonth()).setValue(4);
         $(DateRangePage.dateRangeToYear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a valid date');
         expect($(DateRangePage.errorNumber(2)).isExisting()).to.be.false;
      });

      it('When I enter a year but no month, Then I should see only a single invalid date error', function() {
         $(DateRangePage.dateRangeFromMonth()).setValue(10);
         $(DateRangePage.dateRangeFromYear()).setValue('');

         $(DateRangePage.dateRangeToMonth()).setValue(4);
         $(DateRangePage.dateRangeToYear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a valid date');
         expect($(DateRangePage.errorNumber(2)).isExisting()).to.be.false;
      });

      it('When I enter a year of 0, Then I should see only a single invalid date error', function() {
         $(DateRangePage.dateRangeFromMonth()).setValue(10);
         $(DateRangePage.dateRangeFromYear()).setValue(0);

         $(DateRangePage.dateRangeToMonth()).setValue(4);
         $(DateRangePage.dateRangeToYear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a valid date');
         expect($(DateRangePage.errorNumber(2)).isExisting()).to.be.false;
      });

      it('When I enter a year that contains more than 4 characters, Then I should see only a single invalid date error', function() {
         $(DateRangePage.dateRangeFromMonth()).setValue(10);
         $(DateRangePage.dateRangeFromYear()).setValue(10001);

         $(DateRangePage.dateRangeToMonth()).setValue(4);
         $(DateRangePage.dateRangeToYear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a valid date');
         expect($(DateRangePage.errorNumber(2)).isExisting()).to.be.false;
      });

      it('When I enter a single dates that are too early/late, Then I should see a single validation errors', function() {
         $(DateRangePage.dateRangeFromMonth()).setValue(10);
         $(DateRangePage.dateRangeFromYear()).setValue(2016);

         $(DateRangePage.dateRangeToMonth()).setValue(6);
         $(DateRangePage.dateRangeToYear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a date after November 2016.');
         expect($(DateRangePage.errorNumber(2)).getText()).to.contain('Enter a date before June 2017.');
      });

      it('When I enter a range too large, Then I should see a range validation error', function() {
         $(DateRangePage.dateRangeFromMonth()).setValue(12);
         $(DateRangePage.dateRangeFromYear()).setValue(2016);

         $(DateRangePage.dateRangeToMonth()).setValue(5);
         $(DateRangePage.dateRangeToYear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a reporting period less than or equal to 3 months.');
      });

      it('When I enter a range too small, Then I should see a range validation error', function() {
         $(DateRangePage.dateRangeFromMonth()).setValue(12);
         $(DateRangePage.dateRangeFromYear()).setValue(2016);

         $(DateRangePage.dateRangeToMonth()).setValue(1);
         $(DateRangePage.dateRangeToYear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a reporting period greater than or equal to 2 months.');
      });

      it('When I enter valid dates, Then I should see the summary page', function() {
         $(DateRangePage.dateRangeFromMonth()).setValue(1);
         $(DateRangePage.dateRangeFromYear()).setValue(2017);

         // Min range
         $(DateRangePage.dateRangeToMonth()).setValue(3);
         $(DateRangePage.dateRangeToYear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(SummaryPage.dateRangeFrom()).getText()).to.contain('January 2017 to March 2017');

         // Max range
         $(SummaryPage.dateRangeFromEdit()).click();
         $(DateRangePage.dateRangeToMonth()).setValue(4);
         $(DateRangePage.dateRangeToYear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(SummaryPage.dateRangeFrom()).getText()).to.contain('January 2017 to April 2017');
      });

    });

  });
});

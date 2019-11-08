const DateRangePage = require('../../../../generated_pages/date_validation_combined/date-range-block.page');
const SummaryPage = require('../../../../generated_pages/date_validation_combined/summary.page');

describe('Feature: Combined question level and single validation for dates', function() {
  before(function() {
    browser.openQuestionnaire('test_date_validation_combined.json');
  });

  describe('Period Validation', function () {
    describe('Given I enter dates', function() {

      it('When I enter a single dates that are too early/late, Then I should see a single validation errors', function() {
         $(DateRangePage.dateRangeFromday()).setValue(12);
         $(DateRangePage.dateRangeFrommonth()).setValue(12);
         $(DateRangePage.dateRangeFromyear()).setValue(2016);

         $(DateRangePage.dateRangeToday()).setValue(22);
         $(DateRangePage.dateRangeTomonth()).setValue(2);
         $(DateRangePage.dateRangeToyear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a date after 12 December 2016.');
         expect($(DateRangePage.errorNumber(2)).getText()).to.contain('Enter a date before 22 February 2017.');
      });

      it('When I enter a range too large, Then I should see a range validation error', function() {
         $(DateRangePage.dateRangeFromday()).setValue(13);
         $(DateRangePage.dateRangeFrommonth()).setValue(12);
         $(DateRangePage.dateRangeFromyear()).setValue(2016);

         $(DateRangePage.dateRangeToday()).setValue(21);
         $(DateRangePage.dateRangeTomonth()).setValue(2);
         $(DateRangePage.dateRangeToyear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a reporting period less than or equal to 50 days.');
      });

      it('When I enter a range too small, Then I should see a range validation error', function() {
         $(DateRangePage.dateRangeFromday()).setValue(1);
         $(DateRangePage.dateRangeFrommonth()).setValue(1);
         $(DateRangePage.dateRangeFromyear()).setValue(2017);

         $(DateRangePage.dateRangeToday()).setValue(10);
         $(DateRangePage.dateRangeTomonth()).setValue(1);
         $(DateRangePage.dateRangeToyear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a reporting period greater than or equal to 10 days.');
      });

      it('When I enter valid dates, Then I should see the summary page', function() {
         $(DateRangePage.dateRangeFromday()).setValue(1);
         $(DateRangePage.dateRangeFrommonth()).setValue(1);
         $(DateRangePage.dateRangeFromyear()).setValue(2017);

         // Min range
         $(DateRangePage.dateRangeToday()).setValue(11);
         $(DateRangePage.dateRangeTomonth()).setValue(1);
         $(DateRangePage.dateRangeToyear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(SummaryPage.dateRangeFrom()).getText()).to.contain('1 January 2017 to 11 January 2017');

         // Max range
         $(SummaryPage.dateRangeFromEdit()).click();
         $(DateRangePage.dateRangeToday()).setValue(20);
         $(DateRangePage.dateRangeTomonth()).setValue(2);
         $(DateRangePage.dateRangeToyear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(SummaryPage.dateRangeFrom()).getText()).to.contain('1 January 2017 to 20 February 2017');
      });

    });

  });
});

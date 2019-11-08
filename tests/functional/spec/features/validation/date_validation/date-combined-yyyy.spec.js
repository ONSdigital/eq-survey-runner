const DateRangePage = require('../../../../generated_pages/date_validation_yyyy_combined/date-range-block.page');
const SummaryPage = require('../../../../generated_pages/date_validation_yyyy_combined/summary.page');


describe('Feature: Combined question level and single validation for MM-YYYY dates', function() {
  before(function() {
    browser.openQuestionnaire('test_date_validation_yyyy_combined.json');
  });

  describe('Period Validation', function () {
    describe('Given I enter dates', function() {

      it('When I enter a single dates that are too early/late, Then I should see a single validation errors', function() {
         $(DateRangePage.dateRangeFromYear()).setValue(2015);
         $(DateRangePage.dateRangeToYear()).setValue(2021);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a date after 2015.');
         expect($(DateRangePage.errorNumber(2)).getText()).to.contain('Enter a date before 2021.');
      });

      it('When I enter a range too large, Then I should see a range validation error', function() {
         $(DateRangePage.dateRangeFromYear()).setValue(2016);
         $(DateRangePage.dateRangeToYear()).setValue(2020);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a reporting period less than or equal to 3 years.');
      });

      it('When I enter a range too small, Then I should see a range validation error', function() {
         $(DateRangePage.dateRangeFromYear()).setValue(2016);
         $(DateRangePage.dateRangeToYear()).setValue(2017);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a reporting period greater than or equal to 2 years.');
      });

      it('When I enter an invalid year, Then I should see a single validation error', function() {
         $(DateRangePage.dateRangeFromYear()).setValue(2016);
         $(DateRangePage.dateRangeToYear()).setValue(20167);
         $(DateRangePage.submit()).click();
         expect($(DateRangePage.errorNumber(1)).getText()).to.contain('Enter a valid date.');
         expect($(DateRangePage.errorNumber(2)).isExisting()).to.be.false;
      });

      it('When I enter valid dates, Then I should see the summary page', function() {
         $(DateRangePage.dateRangeFromYear()).setValue(2016);
         // Min range
         $(DateRangePage.dateRangeToYear()).setValue(2018);
         $(DateRangePage.submit()).click();
         expect($(SummaryPage.dateRangeFrom()).getText()).to.contain('2016 to 2018');

         // Max range
         $(SummaryPage.dateRangeFromEdit()).click();
         $(DateRangePage.dateRangeToYear()).setValue(2019);
         $(DateRangePage.submit()).click();
         expect($(SummaryPage.dateRangeFrom()).getText()).to.contain('2016 to 2019');
      });

    });

  });
});

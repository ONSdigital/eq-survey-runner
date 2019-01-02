import {openQuestionnaire} from '../../../../../helpers/helpers.js'
const DateRangePage = require('../../../../../generated_pages/date_validation_mm_yyyy_combined/date-range-block.page');
const SummaryPage = require('../../../../../generated_pages/date_validation_mm_yyyy_combined/summary.page');

describe('Feature: Combined question level and single validation for MM-YYYY dates', function() {

  before(function() {
    return helpers.openQuestionnaire('test_date_validation_mm_yyyy_combined.json');
  });

  describe('Period Validation', function () {
    describe('Given I enter dates', function() {

      it('When I enter a month but no year, Then I should see only a single invalid date error', function() {
                 .get(DateRangePage.dateRangeFromYear()).type(2018)

         .get(DateRangePage.dateRangeToMonth()).select(4)
         .get(DateRangePage.dateRangeToYear()).type(2017)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a valid date')
         .get(DateRangePage.errorNumber(2)).should('not.exist');
      });

      it('When I enter a year but no month, Then I should see only a single invalid date error', function() {
                 .get(DateRangePage.dateRangeFromMonth()).select(10)
         .get(DateRangePage.dateRangeFromYear()).clear()

         .get(DateRangePage.dateRangeToMonth()).select(4)
         .get(DateRangePage.dateRangeToYear()).type(2017)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a valid date')
         .get(DateRangePage.errorNumber(2)).should('not.exist');
      });

      it('When I enter a year of 0, Then I should see only a single invalid date error', function() {
                 .get(DateRangePage.dateRangeFromMonth()).select(10)
         .get(DateRangePage.dateRangeFromYear()).type(0)

         .get(DateRangePage.dateRangeToMonth()).select(4)
         .get(DateRangePage.dateRangeToYear()).type(2017)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a valid date')
         .get(DateRangePage.errorNumber(2)).should('not.exist');
      });

      it('When I enter a year that contains more than 4 characters, Then I should see only a single invalid date error', function() {
                 .get(DateRangePage.dateRangeFromMonth()).select(10)
         .get(DateRangePage.dateRangeFromYear()).type(10001)

         .get(DateRangePage.dateRangeToMonth()).select(4)
         .get(DateRangePage.dateRangeToYear()).type(2017)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a valid date')
         .get(DateRangePage.errorNumber(2)).should('not.exist');
      });

      it('When I enter a single dates that are too early/late, Then I should see a single validation errors', function() {
                 .get(DateRangePage.dateRangeFromMonth()).select(10)
         .get(DateRangePage.dateRangeFromYear()).type(2016)

         .get(DateRangePage.dateRangeToMonth()).select(6)
         .get(DateRangePage.dateRangeToYear()).type(2017)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a date after November 2016.')
         .get(DateRangePage.errorNumber(2)).stripText().should('contain', 'Enter a date before June 2017.');
      });

      it('When I enter a range too large, Then I should see a range validation error', function() {
                 .get(DateRangePage.dateRangeFromMonth()).select(12)
         .get(DateRangePage.dateRangeFromYear()).type(2016)

         .get(DateRangePage.dateRangeToMonth()).select(5)
         .get(DateRangePage.dateRangeToYear()).type(2017)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a reporting period less than or equal to 3 months.');
      });

      it('When I enter a range too small, Then I should see a range validation error', function() {
                 .get(DateRangePage.dateRangeFromMonth()).select(12)
         .get(DateRangePage.dateRangeFromYear()).type(2016)

         .get(DateRangePage.dateRangeToMonth()).select(1)
         .get(DateRangePage.dateRangeToYear()).type(2017)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a reporting period greater than or equal to 2 months.');
      });

      it('When I enter valid dates, Then I should see the summary page', function() {
                 .get(DateRangePage.dateRangeFromMonth()).select(1)
         .get(DateRangePage.dateRangeFromYear()).type(2017)

         // Min range
         .get(DateRangePage.dateRangeToMonth()).select(3)
         .get(DateRangePage.dateRangeToYear()).type(2017)
         .get(DateRangePage.submit()).click()
         .get(SummaryPage.dateRangeFrom()).stripText().should('contain', 'January 2017 to March 2017')

         // Max range
         .get(SummaryPage.dateRangeFromEdit()).click()
         .get(DateRangePage.dateRangeToMonth()).select(4)
         .get(DateRangePage.dateRangeToYear()).type(2017)
         .get(DateRangePage.submit()).click()
         .get(SummaryPage.dateRangeFrom()).stripText().should('contain', 'January 2017 to April 2017');
      });

    });

  });
});

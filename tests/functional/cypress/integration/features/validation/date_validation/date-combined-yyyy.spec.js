import {openQuestionnaire} from '../../../../../helpers/helpers.js'
const DateRangePage = require('../../../../../generated_pages/date_validation_yyyy_combined/date-range-block.page');
var SummaryPage = require('../../../../../generated_pages/date_validation_yyyy_combined/summary.page');

describe('Feature: Combined question level and single validation for MM-YYYY dates', function() {

  before(function() {
    return helpers.openQuestionnaire('test_date_validation_yyyy_combined.json');
  });

  describe('Period Validation', function () {
    describe('Given I enter dates', function() {

      it('When I enter a single dates that are too early/late, Then I should see a single validation errors', function() {
                 .get(DateRangePage.dateRangeFromYear()).type(2015)
         .get(DateRangePage.dateRangeToYear()).type(2021)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a date after 2015.')
         .get(DateRangePage.errorNumber(2)).stripText().should('contain', 'Enter a date before 2021.');
      });

      it('When I enter a range too large, Then I should see a range validation error', function() {
                 .get(DateRangePage.dateRangeFromYear()).type(2016)
         .get(DateRangePage.dateRangeToYear()).type(2020)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a reporting period less than or equal to 3 years.');
      });

      it('When I enter a range too small, Then I should see a range validation error', function() {
                 .get(DateRangePage.dateRangeFromYear()).type(2016)
         .get(DateRangePage.dateRangeToYear()).type(2017)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a reporting period greater than or equal to 2 years.');
      });

      it('When I enter an invalid year, Then I should see a single validation error', function() {
                 .get(DateRangePage.dateRangeFromYear()).type(2016)
         .get(DateRangePage.dateRangeToYear()).type(20167)
         .get(DateRangePage.submit()).click()
         .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a valid date.')
         .get(DateRangePage.errorNumber(2)).should('not.exist');
      });

      it('When I enter valid dates, Then I should see the summary page', function() {
                 .get(DateRangePage.dateRangeFromYear()).type(2016)
         // Min range
         .get(DateRangePage.dateRangeToYear()).type(2018)
         .get(DateRangePage.submit()).click()
         .get(SummaryPage.dateRangeFrom()).stripText().should('contain', '2016 to 2018')

         // Max range
         .get(SummaryPage.dateRangeFromEdit()).click()
         .get(DateRangePage.dateRangeToYear()).type(2019)
         .get(DateRangePage.submit()).click()
         .get(SummaryPage.dateRangeFrom()).stripText().should('contain', '2016 to 2019');
      });

    });

  });
});

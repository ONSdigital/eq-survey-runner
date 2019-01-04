import {openQuestionnaire} from '../../../../helpers/helpers.js';
const DateRangePage = require('../../../../../generated_pages/date_validation_combined/date-range-block.page');
var SummaryPage = require('../../../../../generated_pages/date_validation_combined/summary.page');

describe('Feature: Combined question level and single validation for dates', function() {

  before(function() {
    openQuestionnaire('test_date_validation_combined.json');
  });

  beforeEach(function () {
    // Cypress clears cookies between tests by default.
    Cypress.Cookies.preserveOnce('session');
  });

  describe('Period Validation', function () {
    describe('Given I enter dates', function() {

      it('When I enter a single dates that are too early/late, Then I should see a single validation errors', function() {
        cy
          .get(DateRangePage.dateRangeFromday()).clear().type(12)
          .get(DateRangePage.dateRangeFrommonth()).select('12')
          .get(DateRangePage.dateRangeFromyear()).clear().type(2016)

          .get(DateRangePage.dateRangeToday()).clear().type(22)
          .get(DateRangePage.dateRangeTomonth()).select('2')
          .get(DateRangePage.dateRangeToyear()).clear().type(2017)
          .get(DateRangePage.submit()).click()
          .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a date after 12 December 2016.')
          .get(DateRangePage.errorNumber(2)).stripText().should('contain', 'Enter a date before 22 February 2017.');
      });

      it('When I enter a range too large, Then I should see a range validation error', function() {
        cy
          .get(DateRangePage.dateRangeFromday()).clear().type(13)
          .get(DateRangePage.dateRangeFrommonth()).select('12')
          .get(DateRangePage.dateRangeFromyear()).clear().type(2016)

          .get(DateRangePage.dateRangeToday()).clear().type(21)
          .get(DateRangePage.dateRangeTomonth()).select('2')
          .get(DateRangePage.dateRangeToyear()).clear().type(2017)
          .get(DateRangePage.submit()).click()
          .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a reporting period less than or equal to 50 days.');
      });

      it('When I enter a range too small, Then I should see a range validation error', function() {
        cy
          .get(DateRangePage.dateRangeFromday()).clear().type(1)
          .get(DateRangePage.dateRangeFrommonth()).select('1')
          .get(DateRangePage.dateRangeFromyear()).clear().type(2017)

          .get(DateRangePage.dateRangeToday()).clear().type(10)
          .get(DateRangePage.dateRangeTomonth()).select('1')
          .get(DateRangePage.dateRangeToyear()).clear().type(2017)
          .get(DateRangePage.submit()).click()
          .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a reporting period greater than or equal to 10 days.');
      });

      it('When I enter valid dates, Then I should see the summary page', function() {
        cy
          .get(DateRangePage.dateRangeFromday()).clear().type(1)
          .get(DateRangePage.dateRangeFrommonth()).select('1')
          .get(DateRangePage.dateRangeFromyear()).clear().type(2017)

        // Min range
          .get(DateRangePage.dateRangeToday()).clear().type(11)
          .get(DateRangePage.dateRangeTomonth()).select('1')
          .get(DateRangePage.dateRangeToyear()).clear().type(2017)
          .get(DateRangePage.submit()).click()
          .get(SummaryPage.dateRangeFrom()).stripText().should('contain', '1 January 2017 to 11 January 2017')

        // Max range
          .get(SummaryPage.dateRangeFromEdit()).click()
          .get(DateRangePage.dateRangeToday()).clear().type(20)
          .get(DateRangePage.dateRangeTomonth()).select('2')
          .get(DateRangePage.dateRangeToyear()).clear().type(2017)
          .get(DateRangePage.submit()).click()
          .get(SummaryPage.dateRangeFrom()).stripText().should('contain', '1 January 2017 to 20 February 2017');
      });

    });

  });
});

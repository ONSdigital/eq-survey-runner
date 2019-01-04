import {openQuestionnaire} from '../../../../helpers/helpers.js';

describe('Feature: Question level validation for date ranges', function() {
  var DateRangePage = require('../../../../../generated_pages/date_validation_range/date-range-block.page');
  var SummaryPage = require('../../../../../generated_pages/date_validation_range/summary.page');

  beforeEach(function() {
    openQuestionnaire('test_date_validation_range.json');
  });

  describe('Period Validation', function() {
    describe('Given I enter a date period greater than the max period limit', function() {
      it('When I continue, Then I should see a period validation error', function() {
        cy
          .get(DateRangePage.dateRangeFromday()).type(1)
          .get(DateRangePage.dateRangeFrommonth()).select('1')
          .get(DateRangePage.dateRangeFromyear()).type(2018)

          .get(DateRangePage.dateRangeToday()).type(3)
          .get(DateRangePage.dateRangeTomonth()).select('3')
          .get(DateRangePage.dateRangeToyear()).type(2018)
          .get(DateRangePage.submit()).click()
          .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a reporting period less than or equal to 1 month, 20 days.');
      });
    });

    describe('Given I enter a date period less than the min period limit', function() {
      it('When I continue, Then I should see a period validation error', function() {
        cy
          .get(DateRangePage.dateRangeFromday()).type(1)
          .get(DateRangePage.dateRangeFrommonth()).select('1')
          .get(DateRangePage.dateRangeFromyear()).type(2018)

          .get(DateRangePage.dateRangeToday()).type(3)
          .get(DateRangePage.dateRangeTomonth()).select('1')
          .get(DateRangePage.dateRangeToyear()).type(2018)
          .get(DateRangePage.submit()).click()
          .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a reporting period greater than or equal to 23 days.');
      });
    });

    describe('Given I enter a date period within the set period limits', function() {
      it('When I continue, Then I should be able to reach the summary', function() {
        cy
          .get(DateRangePage.dateRangeFromday()).type(1)
          .get(DateRangePage.dateRangeFrommonth()).select('1')
          .get(DateRangePage.dateRangeFromyear()).type(2018)

          .get(DateRangePage.dateRangeToday()).type(3)
          .get(DateRangePage.dateRangeTomonth()).select('2')
          .get(DateRangePage.dateRangeToyear()).type(2018)
          .get(DateRangePage.submit()).click()
          .url().should('contain', SummaryPage.pageName);
      });
    });
  });

  describe('Date Range Validation', function() {
    describe('Given I enter a "to date" which is earlier than the "from date"', function() {
      it('When I continue, Then I should see a validation error', function() {
        cy
          .get(DateRangePage.dateRangeFromday()).type(1)
          .get(DateRangePage.dateRangeFrommonth()).select('2')
          .get(DateRangePage.dateRangeFromyear()).type(2018)

          .get(DateRangePage.dateRangeToday()).type(3)
          .get(DateRangePage.dateRangeTomonth()).select('1')
          .get(DateRangePage.dateRangeToyear()).type(2018)
          .get(DateRangePage.submit()).click()
          .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a \'period to\' date later than the \'period from\' date.');
      });
    });

    describe('Given I enter matching dates for the "from" and "to" dates', function() {
      it('When I continue, Then I should see a validation error', function() {
        cy
          .get(DateRangePage.dateRangeFromday()).type(1)
          .get(DateRangePage.dateRangeFrommonth()).select('1')
          .get(DateRangePage.dateRangeFromyear()).type(2018)

          .get(DateRangePage.dateRangeToday()).type(1)
          .get(DateRangePage.dateRangeTomonth()).select('1')
          .get(DateRangePage.dateRangeToyear()).type(2018)
          .get(DateRangePage.submit()).click()
          .get(DateRangePage.errorNumber(1)).stripText().should('contain', 'Enter a \'period to\' date later than the \'period from\' date.');
      });
    });

    describe('Given I enter a valid date range', function() {
      it('When I continue, Then I should be able to reach the summary', function() {
        cy
          .get(DateRangePage.dateRangeFromday()).type(1)
          .get(DateRangePage.dateRangeFrommonth()).select('1')
          .get(DateRangePage.dateRangeFromyear()).type(2018)

          .get(DateRangePage.dateRangeToday()).type(3)
          .get(DateRangePage.dateRangeTomonth()).select('2')
          .get(DateRangePage.dateRangeToyear()).type(2018)
          .get(DateRangePage.submit()).click()
          .url().should('contain', SummaryPage.pageName);
      });
    });
  });
});

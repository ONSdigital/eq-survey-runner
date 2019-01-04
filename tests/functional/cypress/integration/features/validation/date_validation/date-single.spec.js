import {openQuestionnaire} from '../../../../helpers/helpers.js';
const DatePage = require('../../../../../generated_pages/date_validation_single/date-block.page');
const DatePeriodPage = require('../../../../../generated_pages/date_validation_single/date-range-block.page');
const SummaryPage = require('../../../../../generated_pages/date_validation_single/summary.page');

describe('Feature: Validation for single date periods', function() {

  beforeEach(function() {
    openQuestionnaire('test_date_validation_single.json');
    completeFirstDatePage();
  });

  describe('Given I enter a date before the minimum offset meta date', function() {
    it('When I continue, Then I should see a period validation error', function() {
      cy
        .get(DatePeriodPage.dateRangeFromday()).type(13)
        .get(DatePeriodPage.dateRangeFrommonth()).select('2')
        .get(DatePeriodPage.dateRangeFromyear()).type(2016)
        .get(DatePeriodPage.submit()).click()

        .get(DatePeriodPage.dateRangeToday()).type(3)
        .get(DatePeriodPage.dateRangeTomonth()).select('3')
        .get(DatePeriodPage.dateRangeToyear()).type(2018)
        .get(DatePeriodPage.submit()).click()
        .get(DatePeriodPage.errorNumber(1)).stripText().should('contain', 'Enter a date after 12 December 2016.');
    });
  });

  describe('Given I enter a date after the maximum offset value date', function() {
    it('When I continue, Then I should see a period validation error', function() {
      cy
        .get(DatePeriodPage.dateRangeFromday()).type(13)
        .get(DatePeriodPage.dateRangeFrommonth()).select('7')
        .get(DatePeriodPage.dateRangeFromyear()).type(2017)
        .get(DatePeriodPage.submit()).click()

        .get(DatePeriodPage.dateRangeToday()).type(3)
        .get(DatePeriodPage.dateRangeTomonth()).select('3')
        .get(DatePeriodPage.dateRangeToyear()).type(2018)
        .get(DatePeriodPage.submit()).click()
        .get(DatePeriodPage.errorNumber(1)).stripText().should('contain', 'Enter a date before 2 July 2017.');
    });
  });

  describe('Given I enter a date before the minimum offset answer id date', function() {
    it('When I continue, Then I should see a period validation error', function() {
      cy
        .get(DatePeriodPage.dateRangeFromday()).type(13)
        .get(DatePeriodPage.dateRangeFrommonth()).select('11')
        .get(DatePeriodPage.dateRangeFromyear()).type(2016)
        .get(DatePeriodPage.submit()).click()

        .get(DatePeriodPage.dateRangeToday()).type(13)
        .get(DatePeriodPage.dateRangeTomonth()).select('1')
        .get(DatePeriodPage.dateRangeToyear()).type(2018)
        .get(DatePeriodPage.submit()).click()
        .get(DatePeriodPage.errorNumber(2)).stripText().should('contain', 'Enter a date after 10 February 2018.');
    });
  });

  describe('Given I enter a date in between the minimum offset meta date and the maximum offset value date', function() {
    it('When I continue, Then I should be able to reach the summary', function() {
      cy
        .get(DatePeriodPage.dateRangeFromday()).type(13)
        .get(DatePeriodPage.dateRangeFrommonth()).select('12')
        .get(DatePeriodPage.dateRangeFromyear()).type(2016)
        .get(DatePeriodPage.submit()).click()

        .get(DatePeriodPage.dateRangeToday()).type(11)
        .get(DatePeriodPage.dateRangeTomonth()).select('2')
        .get(DatePeriodPage.dateRangeToyear()).type(2018)
        .get(DatePeriodPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });
  });

  function completeFirstDatePage() {
    cy
      .get(DatePage.day()).type(1)
      .get(DatePage.month()).select('1')
      .get(DatePage.year()).type(2018)
      .get(DatePage.submit()).click();
  }

});

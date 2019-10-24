const DatePage = require('../../../../generated_pages/date_validation_single/date-block.page');
const DatePeriodPage = require('../../../../generated_pages/date_validation_single/date-range-block.page');
const SummaryPage = require('../../../../generated_pages/date_validation_single/summary.page');

describe('Feature: Validation for single date periods', function() {
  beforeEach(function() {
     browser.openQuestionnaire('test_date_validation_single.json');
     completeFirstDatePage();
  });

  describe('Given I enter a date before the minimum offset meta date', function() {
    it('When I continue, Then I should see a period validation error', function() {
      $(DatePeriodPage.dateRangeFromday()).setValue(13);
      $(DatePeriodPage.dateRangeFrommonth()).setValue(2);
      $(DatePeriodPage.dateRangeFromyear()).setValue(2016);
      $(DatePeriodPage.submit()).click();

      $(DatePeriodPage.dateRangeToday()).setValue(3);
      $(DatePeriodPage.dateRangeTomonth()).setValue(3);
      $(DatePeriodPage.dateRangeToyear()).setValue(2018);
      $(DatePeriodPage.submit()).click();
      expect($(DatePeriodPage.errorNumber(1)).getText()).to.contain('Enter a date after 12 December 2016.');
     });
  });

  describe('Given I enter a date after the maximum offset value date', function() {
    it('When I continue, Then I should see a period validation error', function() {
      $(DatePeriodPage.dateRangeFromday()).setValue(13);
      $(DatePeriodPage.dateRangeFrommonth()).setValue(7);
      $(DatePeriodPage.dateRangeFromyear()).setValue(2017);
      $(DatePeriodPage.submit()).click();

      $(DatePeriodPage.dateRangeToday()).setValue(3);
      $(DatePeriodPage.dateRangeTomonth()).setValue(3);
      $(DatePeriodPage.dateRangeToyear()).setValue(2018);
      $(DatePeriodPage.submit()).click();
      expect($(DatePeriodPage.errorNumber(1)).getText()).to.contain('Enter a date before 2 July 2017.');
     });
  });

  describe('Given I enter a date before the minimum offset answer id date', function() {
    it('When I continue, Then I should see a period validation error', function() {
      $(DatePeriodPage.dateRangeFromday()).setValue(13);
      $(DatePeriodPage.dateRangeFrommonth()).setValue(11);
      $(DatePeriodPage.dateRangeFromyear()).setValue(2016);
      $(DatePeriodPage.submit()).click();

      $(DatePeriodPage.dateRangeToday()).setValue(13);
      $(DatePeriodPage.dateRangeTomonth()).setValue(1);
      $(DatePeriodPage.dateRangeToyear()).setValue(2018);
      $(DatePeriodPage.submit()).click();
      expect($(DatePeriodPage.errorNumber(2)).getText()).to.contain('Enter a date after 10 February 2018.');
     });
  });

  describe('Given I enter a date in between the minimum offset meta date and the maximum offset value date', function() {
    it('When I continue, Then I should be able to reach the summary', function() {
       $(DatePeriodPage.dateRangeFromday()).setValue(13);
       $(DatePeriodPage.dateRangeFrommonth()).setValue(12);
       $(DatePeriodPage.dateRangeFromyear()).setValue(2016);
       $(DatePeriodPage.submit()).click();

       $(DatePeriodPage.dateRangeToday()).setValue(11);
       $(DatePeriodPage.dateRangeTomonth()).setValue(2);
       $(DatePeriodPage.dateRangeToyear()).setValue(2018);
       $(DatePeriodPage.submit()).click();
       expect(browser.getUrl()).to.contain(SummaryPage.pageName);
     });
  });

  function completeFirstDatePage() {
     $(DatePage.day()).setValue(1);
     $(DatePage.month()).setValue(1);
     $(DatePage.year()).setValue(2018);
     $(DatePage.submit()).click();
  }
});

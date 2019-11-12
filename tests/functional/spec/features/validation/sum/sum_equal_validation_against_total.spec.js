const TotalAnswerPage = require('../../../../generated_pages/sum_equal_validation_against_total/total-block.page');
const BreakdownAnswerPage = require('../../../../generated_pages/sum_equal_validation_against_total/breakdown-block.page');
const SummaryPage = require('../../../../generated_pages/sum_equal_validation_against_total/summary.page');

describe('Feature: Sum of grouped answers equal to validation against total ', function () {

  beforeEach(function() {
      browser.openQuestionnaire('test_sum_equal_validation_against_total.json');
  });

  describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
    it('When I continue and enter 3 in each breakdown field, Then I should be able to get to the summary', function() {
      $(TotalAnswerPage.total()).setValue('12');
      $(TotalAnswerPage.submit()).click();
      $(BreakdownAnswerPage.breakdown1()).setValue('3');
      $(BreakdownAnswerPage.breakdown2()).setValue('3');
      $(BreakdownAnswerPage.breakdown3()).setValue('3');
      $(BreakdownAnswerPage.breakdown4()).setValue('3');
      $(BreakdownAnswerPage.submit()).click();
      expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    });
   });

  describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
    it('When I continue and enter 5 into breakdown 1 and leave the others empty, Then I should be able to get to the summary', function() {
      $(TotalAnswerPage.total()).setValue('5');
      $(TotalAnswerPage.submit()).click();
      $(BreakdownAnswerPage.breakdown1()).setValue('5');
      $(BreakdownAnswerPage.breakdown2()).setValue('');
      $(BreakdownAnswerPage.breakdown3()).setValue('');
      $(BreakdownAnswerPage.breakdown4()).setValue('');
      $(BreakdownAnswerPage.submit()).click();
      expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    });
   });

  describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
    it('When I continue and enter 3 in each breakdown field, Then I should see a validation error', function() {
      $(TotalAnswerPage.total()).setValue('5');
      $(TotalAnswerPage.submit()).click();
      $(BreakdownAnswerPage.breakdown1()).setValue('3');
      $(BreakdownAnswerPage.breakdown2()).setValue('3');
      $(BreakdownAnswerPage.breakdown3()).setValue('3');
      $(BreakdownAnswerPage.breakdown4()).setValue('3');
      $(BreakdownAnswerPage.submit()).click();
      expect($(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain('Enter answers that add up to 5');
    });
  });
});


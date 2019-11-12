const TotalAnswerPage = require('../../../../generated_pages/sum_less_validation_against_total/total-block.page');
const BreakdownAnswerPage = require('../../../../generated_pages/sum_less_validation_against_total/breakdown-block.page');
const SummaryPage = require('../../../../generated_pages/sum_less_validation_against_total/summary.page');

describe('Feature: Sum of grouped answers validation (equal or less than) against total', function () {

  beforeEach(function() {
      browser.openQuestionnaire('test_sum_less_validation_against_total.json');
  });

  describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
    it('When I continue and enter 2 in each breakdown field, Then I should be able to get to the summary', function() {
      $(TotalAnswerPage.total()).setValue('12');
      $(TotalAnswerPage.submit()).click();
      $(BreakdownAnswerPage.breakdown1()).setValue('2');
      $(BreakdownAnswerPage.breakdown2()).setValue('2');
      $(BreakdownAnswerPage.breakdown3()).setValue('2');
      $(BreakdownAnswerPage.breakdown4()).setValue('2');
      $(BreakdownAnswerPage.submit()).click();
      expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    });
   });

  describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
    it('When I continue and enter 4 into breakdown 1 and leave the others empty, Then I should be able to get to the summary', function() {
      $(TotalAnswerPage.total()).setValue('5');
      $(TotalAnswerPage.submit()).click();
      $(BreakdownAnswerPage.breakdown1()).setValue('4');
      $(BreakdownAnswerPage.breakdown2()).setValue('');
      $(BreakdownAnswerPage.breakdown3()).setValue('');
      $(BreakdownAnswerPage.breakdown4()).setValue('');
      $(BreakdownAnswerPage.submit()).click();
      expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    });
  });

   describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
    it('When I continue and enter 3 in each breakdown field, Then I should see a validation error', function() {
       $(TotalAnswerPage.total()).setValue('12');
       $(TotalAnswerPage.submit()).click();
       $(BreakdownAnswerPage.breakdown1()).setValue('3');
       $(BreakdownAnswerPage.breakdown2()).setValue('3');
       $(BreakdownAnswerPage.breakdown3()).setValue('3');
       $(BreakdownAnswerPage.breakdown4()).setValue('3');
       $(BreakdownAnswerPage.submit()).click();
       expect($(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain('Enter answers that add up to less than £12.00');
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
       expect($(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain('Enter answers that add up to less than £5.00');
     });
   });
 });


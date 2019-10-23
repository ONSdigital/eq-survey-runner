const helpers = require('../../../../helpers');
const TotalAnswerPage = require('../../../../generated_pages/sum_multi_validation_against_total/total-block.page');
const BreakdownAnswerPage = require('../../../../generated_pages/sum_multi_validation_against_total/breakdown-block.page');
const SummaryPage = require('../../../../generated_pages/sum_multi_validation_against_total/summary.page');

describe('Feature: Sum of grouped answers validation against total (Multi Rule Equals)', function () {
  let browser;

  beforeEach(function() {
      browser = helpers.openQuestionnaire('test_sum_multi_validation_against_total.json').then(openBrowser => browser = openBrowser);
  });

  describe('Given I start a grouped answer with multi rule validation survey and enter 10 into the total', function() {
    it('When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary', function() {
       $(TotalAnswerPage.total()).setValue('10');
       $(TotalAnswerPage.submit()).click();
       $(BreakdownAnswerPage.submit()).click();
       expect(browser.getUrl()).to.contain(SummaryPage.pageName);

       $(SummaryPage.previous()).click();
       $(BreakdownAnswerPage.breakdown1()).setValue('0');
       $(BreakdownAnswerPage.breakdown2()).setValue('0');
       $(BreakdownAnswerPage.breakdown3()).setValue('0');
       $(BreakdownAnswerPage.breakdown4()).setValue('0');
       $(BreakdownAnswerPage.submit()).click();
       expect(browser.getUrl()).to.contain(SummaryPage.pageName);

       $(SummaryPage.previous()).click();
       $(BreakdownAnswerPage.breakdown1()).setValue('1');
       $(BreakdownAnswerPage.breakdown2()).setValue('2');
       $(BreakdownAnswerPage.breakdown3()).setValue('3');
       $(BreakdownAnswerPage.breakdown4()).setValue('4');
       $(BreakdownAnswerPage.submit()).click();
       expect(browser.getUrl()).to.contain(SummaryPage.pageName);
      });
   });

  describe('Given I start a grouped answer with multi rule validation survey and enter 10 into the total', function() {
    it('When I continue and enter less between 1 - 9 or greater than 10, Then it should error', function() {
       $(TotalAnswerPage.total()).setValue('10');
       $(TotalAnswerPage.submit()).click();
       $(BreakdownAnswerPage.breakdown1()).setValue('1');
       $(BreakdownAnswerPage.submit()).click();

       expect($(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain('Enter answers that add up to 10');

       $(BreakdownAnswerPage.breakdown2()).setValue('2');
       $(BreakdownAnswerPage.breakdown3()).setValue('3');
       $(BreakdownAnswerPage.breakdown4()).setValue('5');
       $(BreakdownAnswerPage.submit()).click();
       expect($(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain('Enter answers that add up to 10');
      });
   });
});

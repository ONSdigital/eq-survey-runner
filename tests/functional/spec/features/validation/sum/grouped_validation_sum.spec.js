const helpers = require('../../../../helpers');
const TotalAnswerPage = require('../../../../generated_pages/sum_multi_validation_against_total/total-block.page');
const BreakdownAnswerPage = require('../../../../generated_pages/sum_multi_validation_against_total/breakdown-block.page');
const SummaryPage = require('../../../../generated_pages/sum_multi_validation_against_total/summary.page');

describe('Feature: Sum of grouped answers validation against total (Multi Rule Equals)', function () {

  beforeEach(function() {
      return helpers.openQuestionnaire('test_sum_multi_validation_against_total.json');
  });

  describe('Given I start a grouped answer with multi rule validation survey and enter 10 into the total', function() {
    it('When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary', function() {
      return browser
       .setValue(TotalAnswerPage.total(), '10')
       .click(TotalAnswerPage.submit())
       .click(BreakdownAnswerPage.submit())
       .getUrl().should.eventually.contain(SummaryPage.pageName)

       .click(SummaryPage.previous())
       .setValue(BreakdownAnswerPage.breakdown1(), '0')
       .setValue(BreakdownAnswerPage.breakdown2(), '0')
       .setValue(BreakdownAnswerPage.breakdown3(), '0')
       .setValue(BreakdownAnswerPage.breakdown4(), '0')
       .click(BreakdownAnswerPage.submit())
       .getUrl().should.eventually.contain(SummaryPage.pageName)

       .click(SummaryPage.previous())
       .setValue(BreakdownAnswerPage.breakdown1(), '1')
       .setValue(BreakdownAnswerPage.breakdown2(), '2')
       .setValue(BreakdownAnswerPage.breakdown3(), '3')
       .setValue(BreakdownAnswerPage.breakdown4(), '4')
       .click(BreakdownAnswerPage.submit())
       .getUrl().should.eventually.contain(SummaryPage.pageName);
      });
   });

  describe('Given I start a grouped answer with multi rule validation survey and enter 10 into the total', function() {
    it('When I continue and enter less between 1 - 9 or greater than 10, Then it should error', function() {
      return browser
       .setValue(TotalAnswerPage.total(), '10')
       .click(TotalAnswerPage.submit())
       .setValue(BreakdownAnswerPage.breakdown1(), '1')
       .click(BreakdownAnswerPage.submit())

       .getText(BreakdownAnswerPage.errorNumber(1)).should.eventually.contain('Enter answers that add up to 10')

       .setValue(BreakdownAnswerPage.breakdown2(), '2')
       .setValue(BreakdownAnswerPage.breakdown3(), '3')
       .setValue(BreakdownAnswerPage.breakdown4(), '5')
       .click(BreakdownAnswerPage.submit())
       .getText(BreakdownAnswerPage.errorNumber(1)).should.eventually.contain('Enter answers that add up to 10');
      });
   });
});

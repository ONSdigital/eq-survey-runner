const helpers = require('../../../../helpers');
const TotalAnswerPage = require('../../../../generated_pages/sum_equal_validation_against_total/total-block.page');
const BreakdownAnswerPage = require('../../../../generated_pages/sum_equal_validation_against_total/breakdown-block.page');
const SummaryPage = require('../../../../generated_pages/sum_equal_validation_against_total/summary.page');

describe('Feature: Sum of grouped answers equal to validation against total ', function () {

  beforeEach(function() {
      return helpers.openQuestionnaire('test_sum_equal_validation_against_total.json');
  });

  describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
    it('When I continue and enter 3 in each breakdown field, Then I should be able to get to the summary', function() {
      return browser
       .setValue(TotalAnswerPage.total(), '12')
       .click(TotalAnswerPage.submit())
       .setValue(BreakdownAnswerPage.breakdown1(), '3')
       .setValue(BreakdownAnswerPage.breakdown2(), '3')
       .setValue(BreakdownAnswerPage.breakdown3(), '3')
       .setValue(BreakdownAnswerPage.breakdown4(), '3')
       .click(BreakdownAnswerPage.submit())
       .getUrl().should.eventually.contain(SummaryPage.pageName);
      });
   });

  describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
    it('When I continue and enter 5 into breakdown 1 and leave the others empty, Then I should be able to get to the summary', function() {
      return browser
       .setValue(TotalAnswerPage.total(), '5')
       .click(TotalAnswerPage.submit())
       .setValue(BreakdownAnswerPage.breakdown1(), '5')
       .setValue(BreakdownAnswerPage.breakdown2(), '')
       .setValue(BreakdownAnswerPage.breakdown3(), '')
       .setValue(BreakdownAnswerPage.breakdown4(), '')
       .click(BreakdownAnswerPage.submit())
       .getUrl().should.eventually.contain(SummaryPage.pageName);
      });
   });

   describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
    it('When I continue and enter 3 in each breakdown field, Then I should see a validation error', function() {
      return browser
       .setValue(TotalAnswerPage.total(), '5')
       .click(TotalAnswerPage.submit())
       .setValue(BreakdownAnswerPage.breakdown1(), '3')
       .setValue(BreakdownAnswerPage.breakdown2(), '3')
       .setValue(BreakdownAnswerPage.breakdown3(), '3')
       .setValue(BreakdownAnswerPage.breakdown4(), '3')
       .click(BreakdownAnswerPage.submit())
       .getText(BreakdownAnswerPage.errorNumber(1)).should.eventually.contain('Enter answers that add up to 5');
     });
   });
});


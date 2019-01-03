import {openQuestionnaire} from '../../../../helpers/helpers.js'
const TotalAnswerPage = require('../../../../../generated_pages/sum_multi_validation_against_total/total-block.page');
const BreakdownAnswerPage = require('../../../../../generated_pages/sum_multi_validation_against_total/breakdown-block.page');
const SummaryPage = require('../../../../../generated_pages/sum_multi_validation_against_total/summary.page');

describe('Feature: Sum of grouped answers validation against total (Multi Rule Equals)', function () {

  beforeEach(function() {
    openQuestionnaire('test_sum_multi_validation_against_total.json');
  });

  describe('Given I start a grouped answer with multi rule validation survey and enter 10 into the total', function() {
    it('When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary', function() {
      cy
       .get(TotalAnswerPage.total()).type('10')
       .get(TotalAnswerPage.submit()).click()
       .get(BreakdownAnswerPage.submit()).click()
       .url().should('contain', SummaryPage.pageName)

       .get(SummaryPage.previous()).click()
       .get(BreakdownAnswerPage.breakdown1()).type('0')
       .get(BreakdownAnswerPage.breakdown2()).type('0')
       .get(BreakdownAnswerPage.breakdown3()).type('0')
       .get(BreakdownAnswerPage.breakdown4()).type('0')
       .get(BreakdownAnswerPage.submit()).click()
       .url().should('contain', SummaryPage.pageName)

       .get(SummaryPage.previous()).click()
       .get(BreakdownAnswerPage.breakdown1()).clear().type('1')
       .get(BreakdownAnswerPage.breakdown2()).clear().type('2')
       .get(BreakdownAnswerPage.breakdown3()).clear().type('3')
       .get(BreakdownAnswerPage.breakdown4()).clear().type('4')
       .get(BreakdownAnswerPage.submit()).click()
       .url().should('contain', SummaryPage.pageName);
      });
   });

  describe('Given I start a grouped answer with multi rule validation survey and enter 10 into the total', function() {
    it('When I continue and enter less between 1 - 9 or greater than 10, Then it should error', function() {
      cy
       .get(TotalAnswerPage.total()).type('10')
       .get(TotalAnswerPage.submit()).click()
       .get(BreakdownAnswerPage.breakdown1()).type('1')
       .get(BreakdownAnswerPage.submit()).click()

       .get(BreakdownAnswerPage.errorNumber(1)).stripText().should('contain', 'Enter answers that add up to 10')

       .get(BreakdownAnswerPage.breakdown2()).type('2')
       .get(BreakdownAnswerPage.breakdown3()).type('3')
       .get(BreakdownAnswerPage.breakdown4()).type('5')
       .get(BreakdownAnswerPage.submit()).click()
       .get(BreakdownAnswerPage.errorNumber(1)).stripText().should('contain', 'Enter answers that add up to 10');
      });
   });
});

import {openQuestionnaire} from '../../../../helpers/helpers.js';
const TotalAnswerPage = require('../../../../../generated_pages/sum_less_validation_against_total/total-block.page');
const BreakdownAnswerPage = require('../../../../../generated_pages/sum_less_validation_against_total/breakdown-block.page');
const SummaryPage = require('../../../../../generated_pages/sum_less_validation_against_total/summary.page');

describe('Feature: Sum of grouped answers validation (less than) against total', function () {

  beforeEach(function() {
    openQuestionnaire('test_sum_less_validation_against_total.json');
  });

  describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
    it('When I continue and enter 2 in each breakdown field, Then I should be able to get to the summary', function() {
      cy
        .get(TotalAnswerPage.total()).type('12')
        .get(TotalAnswerPage.submit()).click()
        .get(BreakdownAnswerPage.breakdown1()).type('2')
        .get(BreakdownAnswerPage.breakdown2()).type('2')
        .get(BreakdownAnswerPage.breakdown3()).type('2')
        .get(BreakdownAnswerPage.breakdown4()).type('2')
        .get(BreakdownAnswerPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });
  });

  describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
    it('When I continue and enter 4 into breakdown 1 and leave the others empty, Then I should be able to get to the summary', function() {
      cy
        .get(TotalAnswerPage.total()).type('5')
        .get(TotalAnswerPage.submit()).click()
        .get(BreakdownAnswerPage.breakdown1()).type('4')
        .get(BreakdownAnswerPage.breakdown2()).clear()
        .get(BreakdownAnswerPage.breakdown3()).clear()
        .get(BreakdownAnswerPage.breakdown4()).clear()
        .get(BreakdownAnswerPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });
  });

  describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
    it('When I continue and enter 3 in each breakdown field, Then I should see a validation error', function() {
      cy
        .get(TotalAnswerPage.total()).type('12')
        .get(TotalAnswerPage.submit()).click()
        .get(BreakdownAnswerPage.breakdown1()).type('3')
        .get(BreakdownAnswerPage.breakdown2()).type('3')
        .get(BreakdownAnswerPage.breakdown3()).type('3')
        .get(BreakdownAnswerPage.breakdown4()).type('3')
        .get(BreakdownAnswerPage.submit()).click()
        .get(BreakdownAnswerPage.errorNumber(1)).stripText().should('contain', 'Enter answers that add up to less than £12.00');
    });
  });

  describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
    it('When I continue and enter 3 in each breakdown field, Then I should see a validation error', function() {
      cy
        .get(TotalAnswerPage.total()).type('5')
        .get(TotalAnswerPage.submit()).click()
        .get(BreakdownAnswerPage.breakdown1()).type('3')
        .get(BreakdownAnswerPage.breakdown2()).type('3')
        .get(BreakdownAnswerPage.breakdown3()).type('3')
        .get(BreakdownAnswerPage.breakdown4()).type('3')
        .get(BreakdownAnswerPage.submit()).click()
        .get(BreakdownAnswerPage.errorNumber(1)).stripText().should('contain', 'Enter answers that add up to less than £5.00');
    });
  });
});


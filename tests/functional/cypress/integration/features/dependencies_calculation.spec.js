import {openQuestionnaire} from '../../helpers/helpers.js';
const TotalBlockPage = require('../../../generated_pages/dependencies_calculation/total-block.page.js');
const BreakdownBlockPage = require('../../../generated_pages/dependencies_calculation/breakdown-block.page.js');
const CalculationSummary = require('../../../generated_pages/dependencies_calculation/summary.page.js');

describe('Dependency Calculation', function () {
  describe('Given I complete the test_dependencies_calculation schema', function() {

    beforeEach(function() {
      openQuestionnaire('test_dependencies_calculation.json')
        .get(TotalBlockPage.total()).type(100)
        .get(TotalBlockPage.submit()).click()
        .get(BreakdownBlockPage.breakdown1()).type(10)
        .get(BreakdownBlockPage.breakdown2()).type(20)
        .get(BreakdownBlockPage.breakdown3()).type(30)
        .get(BreakdownBlockPage.breakdown4()).type(40)
        .get(BreakdownBlockPage.submit()).click()
        .get(CalculationSummary.totalAnswerEdit()).click()
        .url().should('contain', TotalBlockPage.pageName);
    });

    it('When I go back and change the total answer Then breakdown block becomes incomplete', function() {
      cy
        .get(TotalBlockPage.total()).type(99)
        .get(TotalBlockPage.submit()).click()
        .navigationLink('Summary').should('not.be.visible');
    });

    it('When I go back and do not change the total answer Then breakdown block remains complete', function() {
      cy
        .get(TotalBlockPage.submit()).click()
        .navigationLink('Summary').should('be.visible');
    });

  });

});

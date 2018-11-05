const helpers = require('../../helpers');
const TotalBlockPage = require('../../generated_pages/dependencies_calculation/total-block.page.js');
const BreakdownBlockPage = require('../../generated_pages/dependencies_calculation/breakdown-block.page.js');
const CalculationSummary = require('../../generated_pages/dependencies_calculation/summary.page.js');

describe('Dependency Calculation', function () {
  describe('Given I complete the test_dependencies_calculation schema', function() {

    beforeEach(function() {
       return helpers.openQuestionnaire('test_dependencies_calculation.json').then(() => {
        return browser
          .setValue(TotalBlockPage.total(),100)
          .click(TotalBlockPage.submit())
          .setValue(BreakdownBlockPage.breakdown1(),10)
          .setValue(BreakdownBlockPage.breakdown2(),20)
          .setValue(BreakdownBlockPage.breakdown3(),30)
          .setValue(BreakdownBlockPage.breakdown4(),40)
          .click(BreakdownBlockPage.submit())
          .click(CalculationSummary.totalAnswerEdit())
          .getUrl().should.eventually.contain(TotalBlockPage.pageName);
       });
    });

    it('When I go back and change the total answer Then breakdown block becomes incomplete', function() {
      return browser
        .setValue(TotalBlockPage.total(),99)
        .click(TotalBlockPage.submit())
        .isVisible(helpers.navigationLink('Summary')).should.eventually.be.false;
    });

    it('When I go back and do not change the total answer Then breakdown block remains complete', function() {
      return browser
        .click(TotalBlockPage.submit())
        .isVisible(helpers.navigationLink('Summary')).should.eventually.be.true;
    });

  });

});

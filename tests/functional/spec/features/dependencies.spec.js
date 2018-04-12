const helpers = require('../../helpers');

describe('Feature: Dependencies', function() {

  describe('Calculation', function () {

    var TotalBlockPage = require('../../pages/features/dependencies/calculation/total-block.page.js');
    var BreakdownBlockPage = require('../../pages/features/dependencies/calculation/breakdown-block.page.js');
    var CalculationSummary = require('../../pages/features/dependencies/calculation/summary.page.js');

    describe('Given I complete the test_dependencies_calculation schema', function() {

      beforeEach(function() {
         return helpers.openQuestionnaire('test_dependencies_calculation.json').then(() => {
          return browser
            .setValue(TotalBlockPage.answer(),100)
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
          .setValue(TotalBlockPage.answer(),99)
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

  describe('Min', function () {

    var MinBlockPage = require('../../pages/features/dependencies/min/min-block.page.js');
    var MinDependentBlockPage = require('../../pages/features/dependencies/min/dependent-block.page.js');
    var MinSummary = require('../../pages/features/dependencies/min/summary.page.js');

    describe('Given I complete the test_dependencies_min_value schema', function() {

      beforeEach(function() {
         return helpers.openQuestionnaire('test_dependencies_min_value.json').then(() => {
          return browser
            .setValue(MinBlockPage.answer(),10)
            .click(MinBlockPage.submit())
            .setValue(MinDependentBlockPage.answer(),10)
            .click(MinDependentBlockPage.submit())
            .click(MinSummary.minAnswerEdit())
            .getUrl().should.eventually.contain(MinBlockPage.pageName);
         });
      });

      it('When I go back and change the minimum answer Then dependent block becomes incomplete', function() {
        return browser
          .setValue(MinBlockPage.answer(),9)
          .click(MinBlockPage.submit())
          .isVisible(helpers.navigationLink('Summary')).should.eventually.be.false;
      });

      it('When I go back and do not change the minimum answer Then dependent block remains complete', function() {
        return browser
          .click(MinBlockPage.submit())
          .isVisible(helpers.navigationLink('Summary')).should.eventually.be.true;
      });

    });

  });

  describe('Max', function () {

    var MaxBlockPage = require('../../pages/features/dependencies/max/max-block.page.js');
    var MaxDependentBlockPage = require('../../pages/features/dependencies/max/dependent-block.page.js');
    var MaxSummary = require('../../pages/features/dependencies/max/summary.page.js');

    describe('Given I complete the test_dependencies_max_value schema', function() {

      beforeEach(function() {
         return helpers.openQuestionnaire('test_dependencies_max_value.json').then(() => {
          return browser
            .setValue(MaxBlockPage.answer(),10)
            .click(MaxBlockPage.submit())
            .setValue(MaxDependentBlockPage.answer(),10)
            .click(MaxDependentBlockPage.submit())
            .click(MaxSummary.maxAnswerEdit())
            .getUrl().should.eventually.contain(MaxBlockPage.pageName);
         });
      });

      it('When I go back and change the maximum answer Then dependent block becomes incomplete', function() {
        return browser
          .setValue(MaxBlockPage.answer(),9)
          .click(MaxBlockPage.submit())
          .isVisible(helpers.navigationLink('Summary')).should.eventually.be.false;
      });

      it('When I go back and do not change the maximum answer Then dependent block remains complete', function() {
        return browser
          .click(MaxBlockPage.submit())
          .isVisible(helpers.navigationLink('Summary')).should.eventually.be.true;
      });

    });

  });

});

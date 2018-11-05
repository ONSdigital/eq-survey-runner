const helpers = require('../../helpers');
const MinBlockPage = require('../../generated_pages/dependencies_min_value/min-block.page.js');
const MinDependentBlockPage = require('../../generated_pages/dependencies_min_value/dependent-block.page.js');
const MinSummary = require('../../generated_pages/dependencies_min_value/summary.page.js');

describe('Dependency Min', function () {
  describe('Given I complete the test_dependencies_min_value schema', function() {

    beforeEach(function() {
      return helpers.openQuestionnaire('test_dependencies_min_value.json').then(() => {
        return browser
          .setValue(MinBlockPage.min(),10)
          .click(MinBlockPage.submit())
          .setValue(MinDependentBlockPage.dependent1(),10)
          .click(MinDependentBlockPage.submit())
          .click(MinSummary.minAnswerEdit())
          .getUrl().should.eventually.contain(MinBlockPage.pageName);
      });
    });

    it('When I go back and change the minimum answer Then dependent block becomes incomplete', function() {
      return browser
        .setValue(MinBlockPage.min(),9)
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

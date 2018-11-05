const helpers = require('../../helpers');
const MaxBlockPage = require('../../generated_pages/dependencies_max_value/max-block.page.js');
const MaxDependentBlockPage = require('../../generated_pages/dependencies_max_value/dependent-block.page.js');
const MaxSummary = require('../../generated_pages/dependencies_max_value/summary.page.js');

describe('Dependency Max', function () {

  describe('Given I complete the test_dependencies_max_value schema', function() {

    beforeEach(function() {
      return helpers.openQuestionnaire('test_dependencies_max_value.json').then(() => {
        return browser
          .setValue(MaxBlockPage.max(), 10)
          .click(MaxBlockPage.submit())
          .setValue(MaxDependentBlockPage.dependent1(),10)
          .click(MaxDependentBlockPage.submit())
          .click(MaxSummary.maxAnswerEdit())
          .getUrl().should.eventually.contain(MaxBlockPage.pageName);
      });
    });

    it('When I go back and change the maximum answer Then dependent block becomes incomplete', function() {
      return browser
        .setValue(MaxBlockPage.max(),9)
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

import {openQuestionnaire} from ../../helpers/helpers.js
const MinBlockPage = require('../../generated_pages/dependencies_min_value/min-block.page.js');
const MinDependentBlockPage = require('../../generated_pages/dependencies_min_value/dependent-block.page.js');
const MinSummary = require('../../generated_pages/dependencies_min_value/summary.page.js');

describe('Dependency Min', function () {
  describe('Given I complete the test_dependencies_min_value schema', function() {

    beforeEach(function() {
      openQuestionnaire('test_dependencies_min_value.json')
                  .get(MinBlockPage.min()).type(10)
          .get(MinBlockPage.submit()).click()
          .get(MinDependentBlockPage.dependent1()).type(10)
          .get(MinDependentBlockPage.submit()).click()
          .get(MinSummary.minAnswerEdit()).click()
          .url().should('contain', MinBlockPage.pageName);
      });
    });

    it('When I go back and change the minimum answer Then dependent block becomes incomplete', function() {
              .get(MinBlockPage.min()).type(9)
        .get(MinBlockPage.submit()).click()
        .isVisible(helpers.navigationLink('Summary')).should.eventually.be.false;
    });

    it('When I go back and do not change the minimum answer Then dependent block remains complete', function() {
              .get(MinBlockPage.submit()).click()
        .isVisible(helpers.navigationLink('Summary')).should.eventually.be.true;
    });

  });

});

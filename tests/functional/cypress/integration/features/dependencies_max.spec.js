import {openQuestionnaire} from '../../helpers/helpers.js';
const MaxBlockPage = require('../../../generated_pages/dependencies_max_value/max-block.page.js');
const MaxDependentBlockPage = require('../../../generated_pages/dependencies_max_value/dependent-block.page.js');
const MaxSummary = require('../../../generated_pages/dependencies_max_value/summary.page.js');

describe('Dependency Max', function () {

  describe('Given I complete the test_dependencies_max_value schema', function() {

    beforeEach(function() {
      openQuestionnaire('test_dependencies_max_value.json')
        .get(MaxBlockPage.max()).type(10)
        .get(MaxBlockPage.submit()).click()
        .get(MaxDependentBlockPage.dependent1()).type(10)
        .get(MaxDependentBlockPage.submit()).click()
        .get(MaxSummary.maxAnswerEdit()).click()
        .url().should('contain', MaxBlockPage.pageName);
    });

    it('When I go back and change the maximum answer Then dependent block becomes incomplete', function() {
      cy
        .get(MaxBlockPage.max()).type(9)
        .get(MaxBlockPage.submit()).click()
        .navigationLink('Summary').should('not.be.visible');
    });

    it('When I go back and do not change the maximum answer Then dependent block remains complete', function() {
      cy
        .get(MaxBlockPage.submit()).click()
        .navigationLink('Summary').should('be.visible');
    });

  });

});

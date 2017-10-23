const helpers = require('../../helpers');

const InvestmentAdvancedMachinery = require('../../pages/surveys/ukis/investment-advanced-machinery.page.js');
const InvestmentExistingKnowledgeInnovation = require('../../pages/surveys/ukis/investment-existing-knowledge-innovation.page.js');

describe('Example Test', function() {

  it('Given I am answering question 3.6 under 3. Innovation Investment block, When I select No as the response, Then I am routed to question 3.9', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .then(() => {
            return helpers.pressSubmit(2);
        })
        .getUrl().should.eventually.contain(InvestmentAdvancedMachinery.pageName)

        // when submit without a response
        .click(InvestmentAdvancedMachinery.submit())
        .getUrl().should.eventually.contain(InvestmentExistingKnowledgeInnovation.pageName)
        .click(InvestmentExistingKnowledgeInnovation.previous())

        // when No selected
        .click(InvestmentAdvancedMachinery.no())
        .click(InvestmentAdvancedMachinery.submit())
        .getUrl().should.eventually.contain(InvestmentExistingKnowledgeInnovation.pageName);
    });
  });

});

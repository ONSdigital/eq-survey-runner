const helpers = require('../../helpers');

const InvestmentExistingKnowledgeInnovation = require('../../pages/surveys/ukis/investment-existing-knowledge-innovation.page.js');
const InvestmentTrainingInnovative = require('../../pages/surveys/ukis/investment-training-innovative.page.js');

describe('Example Test', function() {

  it('Given I am answering question 3.9 under 3. Innovation Investment block, When I don\'t select or select No as the response, Then I am routed to question 3.11', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .then(() => {
            return helpers.pressSubmit(3);
        })
        .getUrl().should.eventually.contain(InvestmentExistingKnowledgeInnovation.pageName)

        // when submit without a response
        .click(InvestmentExistingKnowledgeInnovation.submit())
        .getUrl().should.eventually.contain(InvestmentTrainingInnovative.pageName)
        .click(InvestmentTrainingInnovative.previous())

        // when No selected
        .click(InvestmentExistingKnowledgeInnovation.no())
        .click(InvestmentExistingKnowledgeInnovation.submit())
        .getUrl().should.eventually.contain(InvestmentTrainingInnovative.pageName);
    });
  });

});

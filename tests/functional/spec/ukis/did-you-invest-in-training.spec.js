const helpers = require('../../helpers');

const InvestmentTrainingInnovative = require('../../pages/surveys/ukis/investment-training-innovative.page.js');
const InvestmentDesignFutureInnovation = require('../../pages/surveys/ukis/investment-design-future-innovation.page.js');

describe('Example Test', function() {

  it('Given I am answering question 3.11 under 3. Innovation Investment block, When I  select No as the response, Then I am routed to question 3.13', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .then(() => {
            return helpers.pressSubmit(4);
        })
        .getUrl().should.eventually.contain(InvestmentTrainingInnovative.pageName)

        // when submit without a response
        .click(InvestmentTrainingInnovative.submit())
        .getUrl().should.eventually.contain(InvestmentDesignFutureInnovation.pageName)
        .click(InvestmentDesignFutureInnovation.previous())

        // when No selected
        .click(InvestmentTrainingInnovative.no())
        .click(InvestmentTrainingInnovative.submit())
        .getUrl().should.eventually.contain(InvestmentDesignFutureInnovation.pageName);
    });
  });

});

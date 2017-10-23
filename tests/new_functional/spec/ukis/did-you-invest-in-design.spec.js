const helpers = require('../../helpers');

const InvestmentDesignFutureInnovation = require('../../pages/surveys/ukis/investment-design-future-innovation.page.js');
const InvestmentIntroductionInnovations = require('../../pages/surveys/ukis/investment-introduction-innovations.page.js');

describe('Example Test', function() {

  it('Given I am answering question 3.13 under 3. Innovation Investment block, When I don\'t respond or select No, Then I am routed to question 3.15', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .then(() => {
            return helpers.pressSubmit(5);
        })
        .getUrl().should.eventually.contain(InvestmentDesignFutureInnovation.pageName)

        // when submit without a response
        .click(InvestmentDesignFutureInnovation.submit())
        .getUrl().should.eventually.contain(InvestmentIntroductionInnovations.pageName)
        .click(InvestmentIntroductionInnovations.previous())

        // when No selected
        .click(InvestmentDesignFutureInnovation.no())
        .click(InvestmentDesignFutureInnovation.submit())
        .getUrl().should.eventually.contain(InvestmentIntroductionInnovations.pageName);
    });
  });

});

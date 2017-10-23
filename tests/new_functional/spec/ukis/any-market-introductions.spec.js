const helpers = require('../../helpers');

const InvestmentIntroductionInnovations = require('../../pages/surveys/ukis/investment-introduction-innovations.page.js');
const InnovationInvestmentCompletedPage = require('../../pages/surveys/ukis/innovation-investment-completed.page.js');

describe('Example Test', function() {

  it('Given I am answering question 3.15 under 3. Innovation Investment block, When no response or No is selected, Then I am routed to the interstitial page that comes after 3.17, before Goods & Services questions', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .then(() => {
            return helpers.pressSubmit(6);
        })
        .getUrl().should.eventually.contain(InvestmentIntroductionInnovations.pageName)

        // when submit without a response
        .click(InvestmentIntroductionInnovations.submit())
        .getUrl().should.eventually.contain(InnovationInvestmentCompletedPage.pageName)
        .click(InnovationInvestmentCompletedPage.previous())

        // when No selected
        .click(InvestmentIntroductionInnovations.no())
        .click(InvestmentIntroductionInnovations.submit())
        .getUrl().should.eventually.contain(InnovationInvestmentCompletedPage.pageName);
    });
  });

});

const helpers = require('../../helpers');

const PublicFinancialSupport = require('../../pages/surveys/ukis/public-financial-support.page.js');
const PublicFinancialSupportForInnovationCompleted = require('../../pages/surveys/ukis/public-financial-support-for-innovation-completed.page.js');

describe('Example Test', function() {

  it('Given I am answering question 10.1 under 10. Public Financial Support for Innovation block, When I select No as the response to Central Government Support, Then I am routed to the end of section 10 (interstitial page)', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Public Financial Support for Innovation'))
        .getUrl().should.eventually.contain(PublicFinancialSupport.pageName)
        // when submit without a response
        .click(PublicFinancialSupport.submit())
        .getUrl().should.eventually.contain(PublicFinancialSupportForInnovationCompleted.pageName)
        .click(PublicFinancialSupportForInnovationCompleted.previous())

        // when No selected
        .click(PublicFinancialSupport.centralGovernmentNo())
        .click(PublicFinancialSupport.submit())
        .getUrl().should.eventually.contain(PublicFinancialSupportForInnovationCompleted.pageName);
    });
  });

});

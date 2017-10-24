const helpers = require('../../helpers');

const InternalInvestmentRD = require('../../pages/surveys/ukis/internal-investment-r-d.page.js');
const AcquisitionInternalInvestmentRD = require('../../pages/surveys/ukis/acquisition-internal-investment-r-d.page.js');

describe('Example Test', function() {

  it('Given I am answering question 3.1 under Did you invest in internal R&D? block, When I don\'t respond  or select No, Then I am routed to question 3.4', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .getUrl().should.eventually.contain(InternalInvestmentRD.pageName)

        // when submit without a response
        .click(InternalInvestmentRD.submit())
        .getUrl().should.eventually.contain(AcquisitionInternalInvestmentRD.pageName)
        .click(AcquisitionInternalInvestmentRD.previous())

        // when No selected
        .click(InternalInvestmentRD.no())
        .click(InternalInvestmentRD.submit())
        .getUrl().should.eventually.contain(AcquisitionInternalInvestmentRD.pageName);
    });
  });

});

const helpers = require('../../helpers');

const AcquisitionInternalInvestmentRD = require('../../pages/surveys/ukis/acquisition-internal-investment-r-d.page.js');
const InvestmentAdvancedMachinery = require('../../pages/surveys/ukis/investment-advanced-machinery.page.js');

describe('Example Test', function() {

  it('Given I am answering question 3.4 under 3. Innovation Investment block, When I don\'t select or select No as the response, Then I am routed to question 3.6', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .then(() => {
            return helpers.pressSubmit(1);
        })
        .getUrl().should.eventually.contain(AcquisitionInternalInvestmentRD.pageName)

        // when submit without a response
        .click(AcquisitionInternalInvestmentRD.submit())
        .getUrl().should.eventually.contain(InvestmentAdvancedMachinery.pageName)
        .click(InvestmentAdvancedMachinery.previous())

        // when No selected
        .click(AcquisitionInternalInvestmentRD.no())
        .click(AcquisitionInternalInvestmentRD.submit())
        .getUrl().should.eventually.contain(InvestmentAdvancedMachinery.pageName);
    });
  });

});

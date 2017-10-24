const helpers = require('../../helpers');

const InternalInvestmentRD = require('../../pages/surveys/ukis/internal-investment-r-d.page.js');
const YearsInternalInvestmentRD = require('../../pages/surveys/ukis/years-internal-investment-r-d.page.js');
const ExpenditureInternalInvestmentRD = require('../../pages/surveys/ukis/expenditure-internal-investment-r-d.page.js');
const AcquisitionInternalInvestmentRD = require('../../pages/surveys/ukis/acquisition-internal-investment-r-d.page.js');

describe('Example Test', function() {

  it('Given I am answering question 3.2 under 3. Innovation Investment? block, When I select 2016 in any combination as the response, Then I am routed to question 3.3', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .click(InternalInvestmentRD.yes())
        .click(InternalInvestmentRD.submit())

        // when just 2016
        .click(YearsInternalInvestmentRD.answer2016())
        .click(YearsInternalInvestmentRD.submit())

        // then
        .getUrl().should.eventually.contain(ExpenditureInternalInvestmentRD.pageName)

        // when 2014 and 2016
        .click(ExpenditureInternalInvestmentRD.previous())
        .click(YearsInternalInvestmentRD.answer2014())
        .click(YearsInternalInvestmentRD.submit())
        // then
        .getUrl().should.eventually.contain(ExpenditureInternalInvestmentRD.pageName)

        // when 2015 and 2016
        .click(ExpenditureInternalInvestmentRD.previous())
        .click(YearsInternalInvestmentRD.answer2014())  // Deselect
        .click(YearsInternalInvestmentRD.answer2015())
        .click(YearsInternalInvestmentRD.submit())

        // then
        .getUrl().should.eventually.contain(ExpenditureInternalInvestmentRD.pageName)

        // when all 3
        .click(ExpenditureInternalInvestmentRD.previous())
        .click(YearsInternalInvestmentRD.answer2014())  // Reselect
        .click(YearsInternalInvestmentRD.submit())

                // then
        .getUrl().should.eventually.contain(ExpenditureInternalInvestmentRD.pageName)
    });
  });

  it('Given I am answering question 3.2 under 3. Innovation Investment? block, When no response or I select 2014 or 2015 as the response, Then I am routed to question 3.4', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .click(InternalInvestmentRD.yes())
        .click(InternalInvestmentRD.submit())

        // when no response
        .click(YearsInternalInvestmentRD.submit())
        // then
        .getUrl().should.eventually.contain(AcquisitionInternalInvestmentRD.pageName)

        // when 2014
        .click(AcquisitionInternalInvestmentRD.previous())
        .click(YearsInternalInvestmentRD.answer2014())
        .click(YearsInternalInvestmentRD.submit())
        // then
        .getUrl().should.eventually.contain(AcquisitionInternalInvestmentRD.pageName)

        // when 2015
        .click(AcquisitionInternalInvestmentRD.previous())
        .click(YearsInternalInvestmentRD.answer2014())  // Deselect
        .click(YearsInternalInvestmentRD.answer2015())
        .click(YearsInternalInvestmentRD.submit())
        // then
        .getUrl().should.eventually.contain(AcquisitionInternalInvestmentRD.pageName)
    });
  });

});

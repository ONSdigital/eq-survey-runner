const helpers = require('../helpers');
const HouseTypePage = require('../pages/surveys/section_summary/house-type.page.js');
const InsuranceAddressPage = require('../pages/surveys/section_summary/insurance-address.page.js');
const InsuranceTypePage = require('../pages/surveys/section_summary/insurance-type.page.js');
const AddressDurationPage = require('../pages/surveys/section_summary/address-duration.page.js');
const PropertyDetailsSummaryPage = require('../pages/surveys/section_summary/property-details-summary.page.js');

describe('Section Summary', function() {
  describe('Given I start a Test Section Summary survey', function() {

    const schema = 'test_section_summary.json';

    it('When I have selected a set of answers , Then the selected option should be displayed on the section summary', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
          return browser
           .click(InsuranceTypePage.buildings())
           .click(InsuranceTypePage.submit())
           .click(InsuranceAddressPage.submit())
           .click(AddressDurationPage.yes())
           .click(AddressDurationPage.submit())
           .getText(PropertyDetailsSummaryPage.insuranceTypeAnswer()).should.eventually.contain('Buildings');
      });
    });

  it('When I have selected an answer , And want to change that answer on the section summary, Then the selected option should be displayed on the section summary', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
         return browser
           .click(InsuranceTypePage.buildings())
           .click(InsuranceTypePage.submit())
           .click(InsuranceAddressPage.submit())
           .click(AddressDurationPage.submit())
           .getText(PropertyDetailsSummaryPage.insuranceTypeAnswer()).should.eventually.contain('Buildings')
           .click(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit())
           .click(InsuranceTypePage.contents())
           .click(InsuranceTypePage.submit())
           .click(InsuranceAddressPage.submit())
           .click(AddressDurationPage.submit())
           .getText(PropertyDetailsSummaryPage.insuranceTypeAnswer()).should.eventually.contain('Contents');
      });
    });

   it('When I have selected an answer , And decide to continue on the section summary page, Then I should be taken to the next section', function() {
      return helpers.openQuestionnaire(schema)
        .then(() => {
         return browser
           .click(InsuranceTypePage.buildings())
           .click(InsuranceTypePage.submit())
           .click(InsuranceAddressPage.submit())
           .click(AddressDurationPage.submit())
           .click(PropertyDetailsSummaryPage.submit())
           .getUrl().should.eventually.contain(HouseTypePage.pageName);
        });
    });
  });

});

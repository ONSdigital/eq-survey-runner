const helpers = require('../helpers');
const HouseTypePage = require('../pages/surveys/section_summary/house-type.page.js');
const InsuranceAddressPage = require('../pages/surveys/section_summary/insurance-address.page.js');
const InsuranceTypePage = require('../pages/surveys/section_summary/insurance-type.page.js');
const AddressDurationPage = require('../pages/surveys/section_summary/address-duration.page.js');
const PropertyDetailsSummaryPage = require('../pages/surveys/section_summary/property-details-summary.page.js');
const HouseHoldCompositionPage = require('../pages/surveys/section_summary/household-composition.page.js');
const FinalSummaryPage = require('../pages/surveys/section_summary/final-summary.page.js');

describe('Section Summary', function() {

  describe('Given I start a Test Section Summary survey and complete to Section Summary', function() {

    beforeEach(function() {
      return helpers.openQuestionnaire('test_section_summary.json').then(() => {
        return browser
          .click(InsuranceTypePage.contents())
          .click(InsuranceTypePage.submit())
          .click(InsuranceAddressPage.submit())
          .click(AddressDurationPage.submit())
          .getText(PropertyDetailsSummaryPage.insuranceTypeAnswer()).should.eventually.contain('Contents');
      });
    });

    it('When I have selected an answer to edit and edit it, Then I should return to the section summary with new value displayed', function() {
      return browser
        .click(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit())
        .click(InsuranceTypePage.buildings())
        .click(InsuranceTypePage.submit())
        .getText(PropertyDetailsSummaryPage.insuranceTypeAnswer()).should.eventually.contain('Buildings');
    });

    it('When I continue on the section summary page, Then I should be taken to the next section', function() {
      return browser
        .click(PropertyDetailsSummaryPage.submit())
        .getUrl().should.eventually.contain(HouseHoldCompositionPage.pageName);
    });

  });

  describe('Given I start a Test Section Summary survey and complete to Final Summary', function() {

    beforeEach(function() {
      return helpers.openQuestionnaire('test_section_summary.json').then(() => {
        return browser
          .click(InsuranceTypePage.contents())
          .click(InsuranceTypePage.submit())
          .click(InsuranceAddressPage.submit())
          .click(AddressDurationPage.submit())
          .click(PropertyDetailsSummaryPage.submit())
          .setValue(HouseHoldCompositionPage.firstName(), 'John')
          .click(HouseHoldCompositionPage.submit())
          .getUrl().should.eventually.contain(FinalSummaryPage.pageName);
      });
    });

    it('When I select edit from Final Summary, Then I should be taken back to the Final Summary', function() {
      return browser
        .click(FinalSummaryPage.addressDurationAnswerEdit())
        .click(AddressDurationPage.no())
        .click(AddressDurationPage.submit())
        .getUrl().should.eventually.contain(FinalSummaryPage.pageName);
    });

    it('When I edit from Final Summary but change routing, Then I should be taken back to the Section Summary', function() {
      return browser
        .click(FinalSummaryPage.insuranceTypeAnswerEdit())
        .click(InsuranceTypePage.buildings())
        .click(InsuranceTypePage.submit())
        .getUrl().should.eventually.contain(PropertyDetailsSummaryPage.pageName);
    });

  });

});

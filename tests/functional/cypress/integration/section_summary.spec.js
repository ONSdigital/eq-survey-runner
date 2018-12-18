import {openQuestionnaire} from ../helpers/helpers.js
const InsuranceAddressPage = require('../generated_pages/section_summary/insurance-address.page.js');
const InsuranceTypePage = require('../generated_pages/section_summary/insurance-type.page.js');
const AddressDurationPage = require('../generated_pages/section_summary/address-duration.page.js');
const PropertyDetailsSummaryPage = require('../generated_pages/section_summary/property-details-summary.page.js');
const HouseHoldCompositionPage = require('../generated_pages/section_summary/household-composition.page.js');
const FinalSummaryPage = require('../generated_pages/section_summary/summary.page.js');

describe('Section Summary', function() {

  describe('Given I start a Test Section Summary survey and complete to Section Summary', function() {

    beforeEach(function() {
      openQuestionnaire('test_section_summary.json')
                  .get(InsuranceTypePage.contents()).click()
          .get(InsuranceTypePage.submit()).click()
          .get(InsuranceAddressPage.submit()).click()
          .get(AddressDurationPage.submit()).click()
          .get(PropertyDetailsSummaryPage.insuranceTypeAnswer()).stripText().should('contain', 'Contents');
      });
    });

    it('When I have selected an answer to edit and edit it, Then I should return to the section summary with new value displayed', function() {
              .get(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit()).click()
        .get(InsuranceTypePage.buildings()).click()
        .get(InsuranceTypePage.submit()).click()
        .get(PropertyDetailsSummaryPage.insuranceTypeAnswer()).stripText().should('contain', 'Buildings');
    });

    it('When I continue on the section summary page, Then I should be taken to the next section', function() {
              .get(PropertyDetailsSummaryPage.submit()).click()
        .url().should('contain', HouseHoldCompositionPage.pageName);
    });
  });

  describe('Given I start a Test Section Summary survey and complete to Final Summary', function() {

    beforeEach(function() {
      openQuestionnaire('test_section_summary.json')
                  .get(InsuranceTypePage.contents()).click()
          .get(InsuranceTypePage.submit()).click()
          .get(InsuranceAddressPage.submit()).click()
          .get(AddressDurationPage.submit()).click()
          .get(PropertyDetailsSummaryPage.submit()).click()
          .get(HouseHoldCompositionPage.firstName()).type('John')
          .get(HouseHoldCompositionPage.submit()).click()
          .url().should('contain', FinalSummaryPage.pageName);
      });
    });

    it('When I select edit from Final Summary, Then I should be taken back to the Final Summary', function() {
              .get(FinalSummaryPage.summaryShowAllButton()).click()
        .get(FinalSummaryPage.addressDurationAnswerEdit()).click()
        .get(AddressDurationPage.no()).click()
        .get(AddressDurationPage.submit()).click()
        .url().should('contain', FinalSummaryPage.pageName);
    });

    it('When I edit from Final Summary but change routing, Then I should be taken back to the Section Summary', function() {
              .get(FinalSummaryPage.summaryShowAllButton()).click()
        .get(FinalSummaryPage.insuranceTypeAnswerEdit()).click()
        .get(InsuranceTypePage.buildings()).click()
        .get(InsuranceTypePage.submit()).click()
        .url().should('contain', PropertyDetailsSummaryPage.pageName);
    });

    it('When I click change an answer, Then I should go to that answer', function() {
              .get(FinalSummaryPage.summaryShowAllButton()).click()
        .get(FinalSummaryPage.insuranceTypeAnswer()).stripText().should('contain', 'Contents')
        .get(FinalSummaryPage.insuranceTypeAnswerEdit()).click()
        .url().should('contain', InsuranceTypePage.pageName)
        .get(InsuranceTypePage.buildings()).click()
        .get(InsuranceTypePage.submit()).click()
        .get(FinalSummaryPage.insuranceTypeAnswer()).stripText().should('contain', 'Buildings');
    });
  });

  describe('Given I start a Test Section Summary survey and complete to the first Section Summary', function() {

    it('When I select edit from Section Summary but change routing, Then I should be stepped through the section', function() {
      openQuestionnaire('test_section_summary.json')
                  .get(InsuranceTypePage.both()).click()
          .get(InsuranceTypePage.submit()).click()
          .get(InsuranceAddressPage.submit()).click()
          .get(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit()).click()
          .get(InsuranceTypePage.contents()).click()
          .get(InsuranceTypePage.submit()).click()
          .url().should('contain', InsuranceAddressPage.pageName);
      });
    });
  });
});

const helpers = require('../helpers');
const InsuranceAddressPage = require('../generated_pages/section_summary/insurance-address.page.js');
const InsuranceTypePage = require('../generated_pages/section_summary/insurance-type.page.js');
const AddressDurationPage = require('../generated_pages/section_summary/address-duration.page.js');
const PropertyDetailsSummaryPage = require('../generated_pages/section_summary/property-details-summary.page.js');
const HouseType = require('../generated_pages/section_summary/house-type.page.js');
const HouseholdDetailsSummaryPage = require('../generated_pages/section_summary/household-details-summary.page.js');
const FinalSummaryPage = require('../generated_pages/section_summary/summary.page.js');

describe('Section Summary', function() {

  describe('Given I start a Test Section Summary survey and complete to Section Summary', function() {

    beforeEach(function() {
      return helpers.openQuestionnaire('test_section_summary.json').then(() => {
        return browser
          .click(InsuranceTypePage.both())
          .click(InsuranceTypePage.submit())
          .click(InsuranceAddressPage.submit())
          .getText(PropertyDetailsSummaryPage.insuranceTypeAnswer()).should.eventually.contain('Both');
      });
    });

    it('When I have selected an answer to edit and edit it, Then I should return to the section summary with new value displayed', function() {
      return browser
        .click(PropertyDetailsSummaryPage.insuranceAddressAnswerEdit())
        .setValue(InsuranceAddressPage.answer(), 'Test Address')
        .click(InsuranceAddressPage.submit())
        .getText(PropertyDetailsSummaryPage.insuranceAddressAnswer()).should.eventually.contain('Test Address');
    });

    it('When I continue on the section summary page, Then I should be taken to the next section', function() {
      return browser
        .click(PropertyDetailsSummaryPage.submit())
        .getUrl().should.eventually.contain(HouseType.pageName);
    });

    it('When I select edit from Section Summary but change routing, Then I should be stepped through the section', function() {
      return browser
        .click(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit())
        .click(InsuranceTypePage.contents())
        .click(InsuranceTypePage.submit())
        .getUrl().should.eventually.contain(InsuranceAddressPage.pageName)
        .click(InsuranceAddressPage.submit())
        .getUrl().should.eventually.contain(AddressDurationPage.pageName);
    });
  });

  describe('Given I start a Test Section Summary survey and complete to Section Summary', function() {

    beforeEach(function() {
      return helpers.openQuestionnaire('test_list_collector_section_summary.json').then(() => {
        return browser
          .click(InsuranceTypePage.both())
          .click(InsuranceTypePage.submit())
          .click(InsuranceAddressPage.submit())
          .getText(PropertyDetailsSummaryPage.insuranceTypeAnswer()).should.eventually.contain('Both');
      });
    });

    it('When I have selected an answer to edit and edit it, Then I should return to the section summary with new value displayed', function() {
      return browser
        .click(PropertyDetailsSummaryPage.insuranceAddressAnswerEdit())
        .setValue(InsuranceAddressPage.answer(), 'Test Address')
        .click(InsuranceAddressPage.submit())
        .getText(PropertyDetailsSummaryPage.insuranceAddressAnswer()).should.eventually.contain('Test Address');
    });
  });

  describe('Given I start a Test Section Summary survey and complete to Final Summary', function() {

    beforeEach(function() {
      return helpers.openQuestionnaire('test_section_summary.json').then(() => {
        return browser
          .click(InsuranceTypePage.both())
          .click(InsuranceTypePage.submit())
          .click(InsuranceAddressPage.submit())
          .click(PropertyDetailsSummaryPage.submit())
          .click(HouseType.submit())
          .click(HouseholdDetailsSummaryPage.submit())
          .getUrl().should.eventually.contain(FinalSummaryPage.pageName);
      });
    });

    it('When I select edit from Final Summary and don\'t change an answer, Then I should be taken to the Section Summary', function() {
      return browser
        .click(FinalSummaryPage.summaryShowAllButton())
        .click(FinalSummaryPage.insuranceAddressAnswerEdit())
        .click(InsuranceAddressPage.submit())
        .getUrl().should.eventually.contain(PropertyDetailsSummaryPage.pageName);
    });

    it('When I select edit from Final Summary and change an answer that doesn\'t affect completeness, Then I should be taken to the Section Summary', function() {
      return browser
        .click(FinalSummaryPage.summaryShowAllButton())
        .click(FinalSummaryPage.insuranceAddressAnswerEdit())
        .setValue(InsuranceAddressPage.answer(), 'Test Address')
        .click(InsuranceAddressPage.submit())
        .getUrl().should.eventually.contain(PropertyDetailsSummaryPage.pageName);
    });

    it('When I select edit from Final Summary and change an answer that affects completeness, Then I should be stepped through the section', function() {
      return browser
        .click(FinalSummaryPage.summaryShowAllButton())
        .click(FinalSummaryPage.insuranceTypeAnswerEdit())
        .click(InsuranceTypePage.contents())
        .click(InsuranceTypePage.submit())
        .getUrl().should.eventually.contain(InsuranceAddressPage.pageName)
        .click(InsuranceAddressPage.submit())
        .getUrl().should.eventually.contain(AddressDurationPage.pageName);
    });

    it('When I change an answer, Then the final summary should display the updated value', function() {
      return browser
        .click(FinalSummaryPage.summaryShowAllButton())
        .getText(FinalSummaryPage.insuranceAddressAnswer()).should.eventually.contain('No answer provided')
        .click(FinalSummaryPage.insuranceAddressAnswerEdit())
        .getUrl().should.eventually.contain(InsuranceAddressPage.pageName)
        .setValue(InsuranceAddressPage.answer(), 'Test Address')
        .click(InsuranceAddressPage.submit())
        .getText(FinalSummaryPage.insuranceAddressAnswer()).should.eventually.contain('Test Address');
    });
  });

});

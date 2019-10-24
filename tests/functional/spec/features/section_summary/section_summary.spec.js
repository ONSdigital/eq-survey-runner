const helpers = require('../../../helpers');
const InsuranceAddressPage = require('../../../generated_pages/section_summary/insurance-address.page.js');
const InsuranceTypePage = require('../../../generated_pages/section_summary/insurance-type.page.js');
const AddressDurationPage = require('../../../generated_pages/section_summary/address-duration.page.js');
const PropertyDetailsSummaryPage = require('../../../generated_pages/section_summary/property-details-summary.page.js');
const HouseType = require('../../../generated_pages/section_summary/house-type.page.js');
const HouseholdDetailsSummaryPage = require('../../../generated_pages/section_summary/household-details-summary.page.js');
const FinalSummaryPage = require('../../../generated_pages/section_summary/summary.page.js');

describe('Section Summary', function() {
  let browser;

  describe('Given I start a Test Section Summary survey and complete to Section Summary', function() {

    beforeEach(function() {
      helpers.openQuestionnaire('test_section_summary.json').then(openBrowser => browser = openBrowser);
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      expect($(PropertyDetailsSummaryPage.insuranceTypeAnswer()).getText()).to.contain('Both');
    });

    it('When I have selected an answer to edit and edit it, Then I should return to the section summary with new value displayed', function() {
        $(PropertyDetailsSummaryPage.insuranceAddressAnswerEdit()).click();
        $(InsuranceAddressPage.answer()).setValue('Test Address');
        $(InsuranceAddressPage.submit()).click();
        expect($(PropertyDetailsSummaryPage.insuranceAddressAnswer()).getText()).to.contain('Test Address');
    });

    it('When I continue on the section summary page, Then I should be taken to the next section', function() {
        $(PropertyDetailsSummaryPage.submit()).click();
        expect(browser.getUrl()).to.contain(HouseType.pageName);
    });

    it('When I select edit from Section Summary but change routing, Then I should be stepped through the section', function() {
        $(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit()).click();
        $(InsuranceTypePage.contents()).click();
        $(InsuranceTypePage.submit()).click();
        expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
        $(InsuranceAddressPage.submit()).click();
        expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
    });
  });

  describe('Given I start a Test Section Summary survey and complete to Final Summary', function() {

    beforeEach(function() {
      helpers.openQuestionnaire('test_section_summary.json').then(openBrowser => browser = openBrowser);
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      $(PropertyDetailsSummaryPage.submit()).click();
      $(HouseType.submit()).click();
      $(HouseholdDetailsSummaryPage.submit()).click();
      expect(browser.getUrl()).to.contain(FinalSummaryPage.pageName);
    });

    it('When I select edit from Final Summary and don\'t change an answer, Then I should be taken to the Section Summary', function() {
        $(FinalSummaryPage.summaryShowAllButton()).click();
        $(FinalSummaryPage.insuranceAddressAnswerEdit()).click();
        $(InsuranceAddressPage.submit()).click();
        expect(browser.getUrl()).to.contain(PropertyDetailsSummaryPage.pageName);
    });

    it('When I select edit from Final Summary and change an answer that doesn\'t affect completeness, Then I should be taken to the Section Summary', function() {
        $(FinalSummaryPage.summaryShowAllButton()).click();
        $(FinalSummaryPage.insuranceAddressAnswerEdit()).click();
        $(InsuranceAddressPage.answer()).setValue('Test Address');
        $(InsuranceAddressPage.submit()).click();
        expect(browser.getUrl()).to.contain(PropertyDetailsSummaryPage.pageName);
    });

    it('When I select edit from Final Summary and change an answer that affects completeness, Then I should be stepped through the section', function() {
        $(FinalSummaryPage.summaryShowAllButton()).click();
        $(FinalSummaryPage.insuranceTypeAnswerEdit()).click();
        $(InsuranceTypePage.contents()).click();
        $(InsuranceTypePage.submit()).click();
        expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
        $(InsuranceAddressPage.submit()).click();
        expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
    });

    it('When I change an answer, Then the final summary should display the updated value', function() {
        $(FinalSummaryPage.summaryShowAllButton()).click();
        expect($(FinalSummaryPage.insuranceAddressAnswer()).getText()).to.contain('No answer provided');
        $(FinalSummaryPage.insuranceAddressAnswerEdit()).click();
        expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
        $(InsuranceAddressPage.answer()).setValue('Test Address');
        $(InsuranceAddressPage.submit()).click();
        expect($(FinalSummaryPage.insuranceAddressAnswer()).getText()).to.contain('Test Address');
    });
  });

});

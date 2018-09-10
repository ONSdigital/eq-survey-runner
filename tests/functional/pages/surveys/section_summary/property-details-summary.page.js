// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class PropertyDetailsSummaryPage extends QuestionPage {

  constructor() {
    super('property-details-summary');
  }

  insuranceTypeAnswer(index = 0) { return '#insurance-type-answer-' + index + '-answer'; }

  insuranceTypeAnswerEdit(index = 0) { return '[data-qa="insurance-type-answer-' + index + '-edit"]'; }

  insuranceAddressAnswer(index = 0) { return '#insurance-address-answer-' + index + '-answer'; }

  insuranceAddressAnswerEdit(index = 0) { return '[data-qa="insurance-address-answer-' + index + '-edit"]'; }

  propertyDetailsTitle(index = 0) { return '#property-details-' + index; }

  addressDurationAnswer(index = 0) { return '#address-duration-answer-' + index + '-answer'; }

  addressDurationAnswerEdit(index = 0) { return '[data-qa="address-duration-answer-' + index + '-edit"]'; }

  addressLengthTitle(index = 0) { return '#address-length-' + index; }

  propertyDetailsSectionSummaryTitle(index = 0) { return '#property-details-section-summary-' + index; }

  houseTypeAnswer(index = 0) { return '#house-type-answer-' + index + '-answer'; }

  houseTypeAnswerEdit(index = 0) { return '[data-qa="house-type-answer-' + index + '-edit"]'; }

  houseDetailsTitle(index = 0) { return '#house-details-' + index; }

  householdDetailsSectionSummaryTitle(index = 0) { return '#household-details-section-summary-' + index; }

  lastName(index = 0) { return '#last-name-' + index + '-answer'; }

  lastNameEdit(index = 0) { return '[data-qa="last-name-' + index + '-edit"]'; }

  multipleQuestionsGroupTitle(index = 0) { return '#multiple-questions-group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new PropertyDetailsSummaryPage();

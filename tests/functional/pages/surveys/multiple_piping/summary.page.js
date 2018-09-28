// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  building(index = 0) { return '#building-' + index + '-answer'; }

  buildingEdit(index = 0) { return '[data-qa="building-' + index + '-edit"]'; }

  addressLine1(index = 0) { return '#address-line-1-' + index + '-answer'; }

  addressLine1Edit(index = 0) { return '[data-qa="address-line-1-' + index + '-edit"]'; }

  addressLine2(index = 0) { return '#address-line-2-' + index + '-answer'; }

  addressLine2Edit(index = 0) { return '[data-qa="address-line-2-' + index + '-edit"]'; }

  addressLine3(index = 0) { return '#address-line-3-' + index + '-answer'; }

  addressLine3Edit(index = 0) { return '[data-qa="address-line-3-' + index + '-edit"]'; }

  townCity(index = 0) { return '#town-city-' + index + '-answer'; }

  townCityEdit(index = 0) { return '[data-qa="town-city-' + index + '-edit"]'; }

  county(index = 0) { return '#county-' + index + '-answer'; }

  countyEdit(index = 0) { return '[data-qa="county-' + index + '-edit"]'; }

  postcode(index = 0) { return '#postcode-' + index + '-answer'; }

  postcodeEdit(index = 0) { return '[data-qa="postcode-' + index + '-edit"]'; }

  country(index = 0) { return '#country-' + index + '-answer'; }

  countryEdit(index = 0) { return '[data-qa="country-' + index + '-edit"]'; }

  firstText(index = 0) { return '#first-text-' + index + '-answer'; }

  firstTextEdit(index = 0) { return '[data-qa="first-text-' + index + '-edit"]'; }

  secondText(index = 0) { return '#second-text-' + index + '-answer'; }

  secondTextEdit(index = 0) { return '[data-qa="second-text-' + index + '-edit"]'; }

  multiplePipingAnswer(index = 0) { return '#multiple-piping-answer-' + index + '-answer'; }

  multiplePipingAnswerEdit(index = 0) { return '[data-qa="multiple-piping-answer-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();

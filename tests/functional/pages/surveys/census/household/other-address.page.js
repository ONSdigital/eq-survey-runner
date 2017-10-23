// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class OtherAddressPage extends QuestionPage {

  constructor() {
    super('other-address');
  }

  building() {
    return '#other-address-answer-building';
  }

  buildingLabel() { return '#label-other-address-answer-building'; }

  street() {
    return '#other-address-answer-street';
  }

  streetLabel() { return '#label-other-address-answer-street'; }

  city() {
    return '#other-address-answer-city';
  }

  cityLabel() { return '#label-other-address-answer-city'; }

  county() {
    return '#other-address-answer-county';
  }

  countyLabel() { return '#label-other-address-answer-county'; }

  postcode() {
    return '#other-address-answer-postcode';
  }

  postcodeLabel() { return '#label-other-address-answer-postcode'; }

}
module.exports = new OtherAddressPage();

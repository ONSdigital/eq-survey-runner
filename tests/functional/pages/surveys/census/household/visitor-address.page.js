// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class VisitorAddressPage extends QuestionPage {

  constructor() {
    super('visitor-address');
  }

  building() {
    return '#visitor-address-answer-building';
  }

  buildingLabel() { return '#label-visitor-address-answer-building'; }

  street() {
    return '#visitor-address-answer-street';
  }

  streetLabel() { return '#label-visitor-address-answer-street'; }

  city() {
    return '#visitor-address-answer-city';
  }

  cityLabel() { return '#label-visitor-address-answer-city'; }

  county() {
    return '#visitor-address-answer-county';
  }

  countyLabel() { return '#label-visitor-address-answer-county'; }

  postcode() {
    return '#visitor-address-answer-postcode';
  }

  postcodeLabel() { return '#label-visitor-address-answer-postcode'; }

}
module.exports = new VisitorAddressPage();

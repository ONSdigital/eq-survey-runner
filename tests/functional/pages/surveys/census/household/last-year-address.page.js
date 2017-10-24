// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class LastYearAddressPage extends QuestionPage {

  constructor() {
    super('last-year-address');
  }

  building() {
    return '#last-year-address-answer-building';
  }

  buildingLabel() { return '#label-last-year-address-answer-building'; }

  street() {
    return '#last-year-address-answer-street';
  }

  streetLabel() { return '#label-last-year-address-answer-street'; }

  city() {
    return '#last-year-address-answer-city';
  }

  cityLabel() { return '#label-last-year-address-answer-city'; }

  county() {
    return '#last-year-address-answer-county';
  }

  countyLabel() { return '#label-last-year-address-answer-county'; }

  postcode() {
    return '#last-year-address-answer-postcode';
  }

  postcodeLabel() { return '#label-last-year-address-answer-postcode'; }

}
module.exports = new LastYearAddressPage();

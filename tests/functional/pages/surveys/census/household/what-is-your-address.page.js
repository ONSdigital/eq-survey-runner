// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class WhatIsYourAddressPage extends QuestionPage {

  constructor() {
    super('what-is-your-address');
  }

  building() {
    return '#building';
  }

  buildingLabel() { return '#label-building'; }

  addressLine1() {
    return '#address-line-1';
  }

  addressLine1Label() { return '#label-address-line-1'; }

  addressLine2() {
    return '#address-line-2';
  }

  addressLine2Label() { return '#label-address-line-2'; }

  addressLine3() {
    return '#address-line-3';
  }

  addressLine3Label() { return '#label-address-line-3'; }

  townCity() {
    return '#town-city';
  }

  townCityLabel() { return '#label-town-city'; }

  county() {
    return '#county';
  }

  countyLabel() { return '#label-county'; }

  postcode() {
    return '#postcode';
  }

  postcodeLabel() { return '#label-postcode'; }

  country() {
    return '#country';
  }

  countryLabel() { return '#label-country'; }

}
module.exports = new WhatIsYourAddressPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.858661 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class OtherAddressPage extends QuestionPage {

  setOtherAddressAnswerBuilding(value) {
    browser.setValue('[name="other-address-answer-building"]', value)
    return this
  }

  getOtherAddressAnswerBuilding(value) {
    return browser.element('[name="other-address-answer-building"]').getValue()
  }

  setOtherAddressAnswerStreet(value) {
    browser.setValue('[name="other-address-answer-street"]', value)
    return this
  }

  getOtherAddressAnswerStreet(value) {
    return browser.element('[name="other-address-answer-street"]').getValue()
  }

  setOtherAddressAnswerCity(value) {
    browser.setValue('[name="other-address-answer-city"]', value)
    return this
  }

  getOtherAddressAnswerCity(value) {
    return browser.element('[name="other-address-answer-city"]').getValue()
  }

  setOtherAddressAnswerCounty(value) {
    browser.setValue('[name="other-address-answer-county"]', value)
    return this
  }

  getOtherAddressAnswerCounty(value) {
    return browser.element('[name="other-address-answer-county"]').getValue()
  }

  setOtherAddressAnswerPostcode(value) {
    browser.setValue('[name="other-address-answer-postcode"]', value)
    return this
  }

  getOtherAddressAnswerPostcode(value) {
    return browser.element('[name="other-address-answer-postcode"]').getValue()
  }

}

export default new OtherAddressPage()

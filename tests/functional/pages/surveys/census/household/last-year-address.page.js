// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.905978 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class LastYearAddressPage extends QuestionPage {

  setLastYearAddressAnswerBuilding(value) {
    browser.setValue('[name="last-year-address-answer-building"]', value)
    return this
  }

  getLastYearAddressAnswerBuilding(value) {
    return browser.element('[name="last-year-address-answer-building"]').getValue()
  }

  setLastYearAddressAnswerStreet(value) {
    browser.setValue('[name="last-year-address-answer-street"]', value)
    return this
  }

  getLastYearAddressAnswerStreet(value) {
    return browser.element('[name="last-year-address-answer-street"]').getValue()
  }

  setLastYearAddressAnswerCity(value) {
    browser.setValue('[name="last-year-address-answer-city"]', value)
    return this
  }

  getLastYearAddressAnswerCity(value) {
    return browser.element('[name="last-year-address-answer-city"]').getValue()
  }

  setLastYearAddressAnswerCounty(value) {
    browser.setValue('[name="last-year-address-answer-county"]', value)
    return this
  }

  getLastYearAddressAnswerCounty(value) {
    return browser.element('[name="last-year-address-answer-county"]').getValue()
  }

  setLastYearAddressAnswerPostcode(value) {
    browser.setValue('[name="last-year-address-answer-postcode"]', value)
    return this
  }

  getLastYearAddressAnswerPostcode(value) {
    return browser.element('[name="last-year-address-answer-postcode"]').getValue()
  }

}

export default new LastYearAddressPage()

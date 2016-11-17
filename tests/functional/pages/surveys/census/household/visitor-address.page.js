import QuestionPage from '../../question.page'

class VisitorAddressPage extends QuestionPage {

  setVisitorAddressAnswerBuilding(value) {
    browser.setValue('[name="visitor-address-answer-building"]', value)
    return this
  }

  getVisitorAddressAnswerBuilding(value) {
    return browser.element('[name="visitor-address-answer-building"]').getValue()
  }

  setVisitorAddressAnswerStreet(value) {
    browser.setValue('[name="visitor-address-answer-street"]', value)
    return this
  }

  getVisitorAddressAnswerStreet(value) {
    return browser.element('[name="visitor-address-answer-street"]').getValue()
  }

  setVisitorAddressAnswerCity(value) {
    browser.setValue('[name="visitor-address-answer-city"]', value)
    return this
  }

  getVisitorAddressAnswerCity(value) {
    return browser.element('[name="visitor-address-answer-city"]').getValue()
  }

  setVisitorAddressAnswerCounty(value) {
    browser.setValue('[name="visitor-address-answer-county"]', value)
    return this
  }

  getVisitorAddressAnswerCounty(value) {
    return browser.element('[name="visitor-address-answer-county"]').getValue()
  }

  setVisitorAddressAnswerPostcode(value) {
    browser.setValue('[name="visitor-address-answer-postcode"]', value)
    return this
  }

  getVisitorAddressAnswerPostcode(value) {
    return browser.element('[name="visitor-address-answer-postcode"]').getValue()
  }

}

export default new VisitorAddressPage()

import QuestionPage from '../../question.page'

class CorrectNamePage extends QuestionPage {

  setFirstName(value) {
    browser.setValue('[name="first-name"]', value)
    return this
  }

  getFirstName(value) {
    return browser.element('[name="first-name"]').getValue()
  }

  setMiddleNames(value) {
    browser.setValue('[name="middle-names"]', value)
    return this
  }

  getMiddleNames(value) {
    return browser.element('[name="middle-names"]').getValue()
  }

  setLastName(value) {
    browser.setValue('[name="last-name"]', value)
    return this
  }

  getLastName(value) {
    return browser.element('[name="last-name"]').getValue()
  }

}

export default new CorrectNamePage()

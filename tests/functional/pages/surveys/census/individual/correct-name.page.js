import QuestionPage from '../../question.page'

class CorrectNamePage extends QuestionPage {

  setFirstName(value) {
    browser.setValue('[name="first-name"]', value)
    return this
  }

  setMiddleNames(value) {
    browser.setValue('[name="middle-names"]', value)
    return this
  }

  setLastName(value) {
    browser.setValue('[name="last-name"]', value)
    return this
  }

  getCorrectNameAnswer(value) {
    return browser.element('[name="correct-name-answer"]').getValue()
  }

}

export default new CorrectNamePage()

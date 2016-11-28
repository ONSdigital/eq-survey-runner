import QuestionPage from '../../question.page'

class CorrectNamePage extends QuestionPage {

  setCorrectNameAnswer(value) {
    browser.setValue('[name="correct-name-answer"]', value)
    return this
  }

  getCorrectNameAnswer(value) {
    return browser.element('[name="correct-name-answer"]').getValue()
  }

}

export default new CorrectNamePage()

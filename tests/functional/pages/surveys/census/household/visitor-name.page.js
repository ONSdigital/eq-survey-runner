import QuestionPage from '../../question.page'

class VisitorNamePage extends QuestionPage {

  setVisitorNameAnswer(value) {
    browser.setValue('[name="visitor-name-answer"]', value)
    return this
  }

  getVisitorNameAnswer(value) {
    return browser.element('[name="visitor-name-answer"]').getValue()
  }

}

export default new VisitorNamePage()

import QuestionPage from '../../question.page'

class NumberOfVisitorsPage extends QuestionPage {

  setNumberOfVisitorsAnswer(value) {
    browser.setValue('[name="number-of-visitors-answer"]', value)
    return this
  }

  getNumberOfVisitorsAnswer(value) {
    return browser.element('[name="number-of-visitors-answer"]').getValue()
  }

}

export default new NumberOfVisitorsPage()

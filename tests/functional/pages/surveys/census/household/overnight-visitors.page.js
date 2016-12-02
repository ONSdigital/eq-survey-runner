import QuestionPage from '../../question.page'

class OvernightVisitorsPage extends QuestionPage {

  setOvernightVisitorsAnswer(value) {
    browser.setValue('[name="overnight-visitors-answer"]', value)
    return this
  }

  getOvernightVisitorsAnswer(value) {
    return browser.element('[name="overnight-visitors-answer"]').getValue()
  }

}

export default new OvernightVisitorsPage()

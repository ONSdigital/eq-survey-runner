import QuestionPage from '../../question.page'

class UsualResidentsNumberPage extends QuestionPage {

  setUsualResidentsNumberAnswer(value) {
    browser.setValue('[name="usual-residents-number-answer"]', value)
    return this
  }

  getUsualResidentsNumberAnswer(value) {
    return browser.element('[name="usual-residents-number-answer"]').getValue()
  }

}

export default new UsualResidentsNumberPage()

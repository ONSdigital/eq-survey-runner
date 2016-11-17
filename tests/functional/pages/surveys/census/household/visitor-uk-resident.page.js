import QuestionPage from '../../question.page'

class VisitorUkResidentPage extends QuestionPage {

  clickYes() {
    browser.element('[id="visitor-uk-resident-answer-1"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="visitor-uk-resident-answer-2"]').click()
    return this
  }

  setVisitorUkResidentAnswer(value) {
    browser.setValue('[name="visitor-uk-resident-answer"]', value)
    return this
  }

  getVisitorUkResidentAnswer(value) {
    return browser.element('[name="visitor-uk-resident-answer"]').getValue()
  }

}

export default new VisitorUkResidentPage()

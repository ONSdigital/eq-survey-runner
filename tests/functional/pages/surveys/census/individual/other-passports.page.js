import QuestionPage from '../../question.page'

class OtherPassportsPage extends QuestionPage {

  setOtherPassportsAnswer(value) {
    browser.setValue('[name="other-passports-answer"]', value)
    return this
  }

  getOtherPassportsAnswer(value) {
    return browser.element('[name="other-passports-answer"]').getValue()
  }

}

export default new OtherPassportsPage()

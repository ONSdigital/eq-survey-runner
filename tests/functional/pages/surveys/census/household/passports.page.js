import QuestionPage from '../../question.page'

class PassportsPage extends QuestionPage {

  clickUnitedKingdom() {
    browser.element('[id="passports-answer-1"]').click()
    return this
  }

  clickIrish() {
    browser.element('[id="passports-answer-2"]').click()
    return this
  }

  clickNone() {
    browser.element('[id="passports-answer-3"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="passports-answer-4"]').click()
    return this
  }

  setPassportsAnswer(value) {
    browser.setValue('[name="passports-answer"]', value)
    return this
  }

  getPassportsAnswer(value) {
    return browser.element('[name="passports-answer"]').getValue()
  }

}

export default new PassportsPage()

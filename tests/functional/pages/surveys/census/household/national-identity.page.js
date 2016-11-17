import QuestionPage from '../../question.page'

class NationalIdentityPage extends QuestionPage {

  clickEnglish() {
    browser.element('[id="national-identity-answer-1"]').click()
    return this
  }

  clickWelsh() {
    browser.element('[id="national-identity-answer-2"]').click()
    return this
  }

  clickScottish() {
    browser.element('[id="national-identity-answer-3"]').click()
    return this
  }

  clickNorthernIrish() {
    browser.element('[id="national-identity-answer-4"]').click()
    return this
  }

  clickBritish() {
    browser.element('[id="national-identity-answer-5"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="national-identity-answer-6"]').click()
    return this
  }

  setNationalIdentityAnswer(value) {
    browser.setValue('[name="national-identity-answer"]', value)
    return this
  }

  getNationalIdentityAnswer(value) {
    return browser.element('[name="national-identity-answer"]').getValue()
  }

}

export default new NationalIdentityPage()

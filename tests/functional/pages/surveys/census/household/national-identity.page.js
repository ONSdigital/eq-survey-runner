import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class NationalIdentityPage extends MultipleChoiceWithOtherPage {

  clickNationalIdentityAnswerEnglish() {
    browser.element('[id="national-identity-answer-1"]').click()
    return this
  }

  clickNationalIdentityAnswerWelsh() {
    browser.element('[id="national-identity-answer-2"]').click()
    return this
  }

  clickNationalIdentityAnswerScottish() {
    browser.element('[id="national-identity-answer-3"]').click()
    return this
  }

  clickNationalIdentityAnswerNorthernIrish() {
    browser.element('[id="national-identity-answer-4"]').click()
    return this
  }

  clickNationalIdentityAnswerBritish() {
    browser.element('[id="national-identity-answer-5"]').click()
    return this
  }

  clickNationalIdentityAnswerOther() {
    browser.element('[id="national-identity-answer-6"]').click()
    return this
  }

}

export default new NationalIdentityPage()

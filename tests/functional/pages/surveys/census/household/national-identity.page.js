import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class NationalIdentityPage extends MultipleChoiceWithOtherPage {

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

}

export default new NationalIdentityPage()

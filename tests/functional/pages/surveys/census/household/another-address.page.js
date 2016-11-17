import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AnotherAddressPage extends MultipleChoiceWithOtherPage {

  clickNo() {
    browser.element('[id="another-address-answer-1"]').click()
    return this
  }

  clickYesAnAddressWithinTheUk() {
    browser.element('[id="another-address-answer-2"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="another-address-answer-3"]').click()
    return this
  }

  setAnotherAddressAnswer(value) {
    browser.setValue('[name="another-address-answer"]', value)
    return this
  }

  getAnotherAddressAnswer(value) {
    return browser.element('[name="another-address-answer"]').getValue()
  }

}

export default new AnotherAddressPage()

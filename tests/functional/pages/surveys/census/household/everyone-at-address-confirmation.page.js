import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EveryoneAtAddressConfirmationPage extends MultipleChoiceWithOtherPage {

  clickYes() {
    browser.element('[id="everyone-at-address-confirmation-answer-1"]').click()
    return this
  }

  clickNoINeedToAddAnotherPerson() {
    browser.element('[id="everyone-at-address-confirmation-answer-2"]').click()
    return this
  }

  setEveryoneAtAddressConfirmationAnswer(value) {
    browser.setValue('[name="everyone-at-address-confirmation-answer"]', value)
    return this
  }

  getEveryoneAtAddressConfirmationAnswer(value) {
    return browser.element('[name="everyone-at-address-confirmation-answer"]').getValue()
  }

}

export default new EveryoneAtAddressConfirmationPage()

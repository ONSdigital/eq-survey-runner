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

}

export default new EveryoneAtAddressConfirmationPage()

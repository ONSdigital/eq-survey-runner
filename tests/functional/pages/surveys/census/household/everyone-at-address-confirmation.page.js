import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EveryoneAtAddressConfirmationPage extends MultipleChoiceWithOtherPage {

  clickEveryoneAtAddressConfirmationAnswerYes() {
    browser.element('[id="everyone-at-address-confirmation-answer-1"]').click()
    return this
  }

  clickEveryoneAtAddressConfirmationAnswerNoINeedToAddAnotherPerson() {
    browser.element('[id="everyone-at-address-confirmation-answer-2"]').click()
    return this
  }

}

export default new EveryoneAtAddressConfirmationPage()

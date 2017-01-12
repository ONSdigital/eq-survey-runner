// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EveryoneAtAddressConfirmationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('everyone-at-address-confirmation')
  }

  clickEveryoneAtAddressConfirmationAnswerYes() {
    browser.element('[id="everyone-at-address-confirmation-answer-0"]').click()
    return this
  }

  clickEveryoneAtAddressConfirmationAnswerNoINeedToAddAnotherPerson() {
    browser.element('[id="everyone-at-address-confirmation-answer-1"]').click()
    return this
  }

}

export default new EveryoneAtAddressConfirmationPage()

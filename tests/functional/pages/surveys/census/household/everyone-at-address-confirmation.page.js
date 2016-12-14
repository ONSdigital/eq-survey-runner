// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.726093 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EveryoneAtAddressConfirmationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('everyone-at-address-confirmation')
  }

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

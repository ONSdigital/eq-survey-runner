// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.824065 - DO NOT EDIT!!! <<<

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

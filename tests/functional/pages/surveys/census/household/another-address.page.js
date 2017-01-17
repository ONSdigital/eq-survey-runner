// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AnotherAddressPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('another-address')
  }

  clickAnotherAddressAnswerNo() {
    browser.element('[id="another-address-answer-0"]').click()
    return this
  }

  clickAnotherAddressAnswerYesAnAddressWithinTheUk() {
    browser.element('[id="another-address-answer-1"]').click()
    return this
  }

  clickAnotherAddressAnswerOther() {
    browser.element('[id="another-address-answer-2"]').click()
    return this
  }

  setAnotherAddressAnswerOtherText(value) {
    browser.setValue('[id="another-address-answer-other"]', value)
    return this
  }

}

export default new AnotherAddressPage()

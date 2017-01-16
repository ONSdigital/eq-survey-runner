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

  setAnotherAddressAnswerOther(value) {
    browser.setValue('[name="another-address-answer-other"]', value)
    return this
  }

  getAnotherAddressAnswerOther(value) {
    return browser.element('[name="another-address-answer-other"]').getValue()
  }

}

export default new AnotherAddressPage()

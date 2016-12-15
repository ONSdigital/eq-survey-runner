// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.766596 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AnotherAddressPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('another-address')
  }

  clickAnotherAddressAnswerNo() {
    browser.element('[id="another-address-answer-1"]').click()
    return this
  }

  clickAnotherAddressAnswerYesAnAddressWithinTheUk() {
    browser.element('[id="another-address-answer-2"]').click()
    return this
  }

  clickAnotherAddressAnswerOther() {
    browser.element('[id="another-address-answer-3"]').click()
    return this
  }

}

export default new AnotherAddressPage()

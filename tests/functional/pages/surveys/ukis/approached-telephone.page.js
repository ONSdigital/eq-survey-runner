// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ApproachedTelephonePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('approached-telephone')
  }

  clickApproachedTelephoneAnswerYes() {
    browser.element('[id="approached-telephone-answer-0"]').click()
    return this
  }

  clickApproachedTelephoneAnswerNo() {
    browser.element('[id="approached-telephone-answer-1"]').click()
    return this
  }

}

export default new ApproachedTelephonePage()

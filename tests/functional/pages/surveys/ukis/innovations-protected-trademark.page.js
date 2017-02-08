// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InnovationsProtectedTrademarkPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('innovations-protected-trademark')
  }

  clickInnovationsProtectedTrademarkAnswerNone() {
    browser.element('[id="innovations-protected-trademark-answer-0"]').click()
    return this
  }

  clickInnovationsProtectedTrademarkAnswerLessThan40() {
    browser.element('[id="innovations-protected-trademark-answer-1"]').click()
    return this
  }

  clickInnovationsProtectedTrademarkAnswer4090() {
    browser.element('[id="innovations-protected-trademark-answer-2"]').click()
    return this
  }

  clickInnovationsProtectedTrademarkAnswerOver90() {
    browser.element('[id="innovations-protected-trademark-answer-3"]').click()
    return this
  }

}

export default new InnovationsProtectedTrademarkPage()

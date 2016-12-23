// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InnovationsProtectedSecrecyPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('innovations-protected-secrecy')
  }

  clickInnovationsProtectedSecrecyAnswerNone() {
    browser.element('[id="innovations-protected-secrecy-answer-0"]').click()
    return this
  }

  clickInnovationsProtectedSecrecyAnswerLessThan40() {
    browser.element('[id="innovations-protected-secrecy-answer-1"]').click()
    return this
  }

  clickInnovationsProtectedSecrecyAnswer4090() {
    browser.element('[id="innovations-protected-secrecy-answer-2"]').click()
    return this
  }

  clickInnovationsProtectedSecrecyAnswerOver90() {
    browser.element('[id="innovations-protected-secrecy-answer-3"]').click()
    return this
  }

}

export default new InnovationsProtectedSecrecyPage()

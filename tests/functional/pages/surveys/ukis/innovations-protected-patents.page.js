// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InnovationsProtectedPatentsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('innovations-protected-patents')
  }

  clickInnovationsProtectedPatentsAnswerNone() {
    browser.element('[id="innovations-protected-patents-answer-0"]').click()
    return this
  }

  clickInnovationsProtectedPatentsAnswerLessThan40() {
    browser.element('[id="innovations-protected-patents-answer-1"]').click()
    return this
  }

  clickInnovationsProtectedPatentsAnswer4090() {
    browser.element('[id="innovations-protected-patents-answer-2"]').click()
    return this
  }

  clickInnovationsProtectedPatentsAnswerOver90() {
    browser.element('[id="innovations-protected-patents-answer-3"]').click()
    return this
  }

}

export default new InnovationsProtectedPatentsPage()

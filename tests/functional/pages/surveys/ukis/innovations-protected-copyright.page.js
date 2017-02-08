// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InnovationsProtectedCopyrightPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('innovations-protected-copyright')
  }

  clickInnovationsProtectedCopyrightAnswerNone() {
    browser.element('[id="innovations-protected-copyright-answer-0"]').click()
    return this
  }

  clickInnovationsProtectedCopyrightAnswerLessThan40() {
    browser.element('[id="innovations-protected-copyright-answer-1"]').click()
    return this
  }

  clickInnovationsProtectedCopyrightAnswer4090() {
    browser.element('[id="innovations-protected-copyright-answer-2"]').click()
    return this
  }

  clickInnovationsProtectedCopyrightAnswerOver90() {
    browser.element('[id="innovations-protected-copyright-answer-3"]').click()
    return this
  }

}

export default new InnovationsProtectedCopyrightPage()

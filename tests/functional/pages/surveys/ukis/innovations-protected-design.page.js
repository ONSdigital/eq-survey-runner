// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InnovationsProtectedDesignPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('innovations-protected-design')
  }

  clickInnovationsProtectedDesignAnswerNone() {
    browser.element('[id="innovations-protected-design-answer-0"]').click()
    return this
  }

  clickInnovationsProtectedDesignAnswerLessThan40() {
    browser.element('[id="innovations-protected-design-answer-1"]').click()
    return this
  }

  clickInnovationsProtectedDesignAnswer4090() {
    browser.element('[id="innovations-protected-design-answer-2"]').click()
    return this
  }

  clickInnovationsProtectedDesignAnswerOver90() {
    browser.element('[id="innovations-protected-design-answer-3"]').click()
    return this
  }

}

export default new InnovationsProtectedDesignPage()

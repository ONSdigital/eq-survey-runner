// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InnovationsProtectedLeadTimePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('innovations-protected-lead-time')
  }

  clickInnovationsProtectedLeadTimeAnswerNone() {
    browser.element('[id="innovations-protected-lead-time-answer-0"]').click()
    return this
  }

  clickInnovationsProtectedLeadTimeAnswerLessThan40() {
    browser.element('[id="innovations-protected-lead-time-answer-1"]').click()
    return this
  }

  clickInnovationsProtectedLeadTimeAnswer4090() {
    browser.element('[id="innovations-protected-lead-time-answer-2"]').click()
    return this
  }

  clickInnovationsProtectedLeadTimeAnswerOver90() {
    browser.element('[id="innovations-protected-lead-time-answer-3"]').click()
    return this
  }

}

export default new InnovationsProtectedLeadTimePage()

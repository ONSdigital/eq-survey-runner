// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImprovedProcessesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('improved-processes')
  }

  clickImprovedProcessesAnswerYes() {
    browser.element('[id="improved-processes-answer-0"]').click()
    return this
  }

  clickImprovedProcessesAnswerNo() {
    browser.element('[id="improved-processes-answer-1"]').click()
    return this
  }

}

export default new ImprovedProcessesPage()

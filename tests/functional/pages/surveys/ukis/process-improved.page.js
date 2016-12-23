// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ProcessImprovedPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('process-improved')
  }

  clickProcessImprovedAnswerYes() {
    browser.element('[id="process-improved-answer-0"]').click()
    return this
  }

  clickProcessImprovedAnswerNo() {
    browser.element('[id="process-improved-answer-1"]').click()
    return this
  }

}

export default new ProcessImprovedPage()

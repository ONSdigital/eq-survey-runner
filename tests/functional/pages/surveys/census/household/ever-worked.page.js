// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EverWorkedPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('ever-worked')
  }

  clickEverWorkedAnswerYes() {
    browser.element('[id="ever-worked-answer-0"]').click()
    return this
  }

  clickEverWorkedAnswerNo() {
    browser.element('[id="ever-worked-answer-1"]').click()
    return this
  }

}

export default new EverWorkedPage()

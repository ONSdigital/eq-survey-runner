// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.857855 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EverWorkedPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('ever-worked')
  }

  clickEverWorkedAnswerYes() {
    browser.element('[id="ever-worked-answer-1"]').click()
    return this
  }

  clickEverWorkedAnswerNo() {
    browser.element('[id="ever-worked-answer-2"]').click()
    return this
  }

}

export default new EverWorkedPage()

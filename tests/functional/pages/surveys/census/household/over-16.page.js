// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class Over16Page extends MultipleChoiceWithOtherPage {

  constructor() {
    super('over-16')
  }

  clickOver16AnswerYes() {
    browser.element('[id="over-16-answer-0"]').click()
    return this
  }

  clickOver16AnswerNo() {
    browser.element('[id="over-16-answer-1"]').click()
    return this
  }

}

export default new Over16Page()

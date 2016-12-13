// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.844628 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class Over16Page extends MultipleChoiceWithOtherPage {

  clickOver16AnswerYes() {
    browser.element('[id="over-16-answer-1"]').click()
    return this
  }

  clickOver16AnswerNo() {
    browser.element('[id="over-16-answer-2"]').click()
    return this
  }

}

export default new Over16Page()

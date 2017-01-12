// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class FurtherContactPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('further-contact')
  }

  clickFurtherContactAnswerYes() {
    browser.element('[id="further-contact-answer-0"]').click()
    return this
  }

  clickFurtherContactAnswerNo() {
    browser.element('[id="further-contact-answer-1"]').click()
    return this
  }

}

export default new FurtherContactPage()

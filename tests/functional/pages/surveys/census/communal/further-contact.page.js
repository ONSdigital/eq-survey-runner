// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-14 14:19:14.086947 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class FurtherContactPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('further-contact')
  }

  clickFurtherContactAnswerYes() {
    browser.element('[id="further-contact-answer-1"]').click()
    return this
  }

  clickFurtherContactAnswerNo() {
    browser.element('[id="further-contact-answer-2"]').click()
    return this
  }

}

export default new FurtherContactPage()

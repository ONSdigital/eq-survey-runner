// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class OtherEthnicGroupPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('other-ethnic-group')
  }

  clickOtherEthnicGroupAnswerArab() {
    browser.element('[id="other-ethnic-group-answer-0"]').click()
    return this
  }

  clickOtherEthnicGroupAnswerOther() {
    browser.element('[id="other-ethnic-group-answer-1"]').click()
    return this
  }

}

export default new OtherEthnicGroupPage()

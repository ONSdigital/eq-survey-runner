// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class OtherEthnicGroupPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('other-ethnic-group')
  }

  clickOtherEthnicGroupAnswerArab() {
    browser.element('[id="other-ethnic-group-answer-1"]').click()
    return this
  }

  clickOtherEthnicGroupAnswerOther() {
    browser.element('[id="other-ethnic-group-answer-2"]').click()
    return this
  }

  setOtherEthnicGroupAnswerOtherText(value) {
    browser.setValue('[id="other-ethnic-group-answer-2-other"]', value)
    return this
  }

}

export default new OtherEthnicGroupPage()

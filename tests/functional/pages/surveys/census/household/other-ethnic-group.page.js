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

  setOtherEthnicGroupAnswerOther(value) {
    browser.setValue('[name="other-ethnic-group-answer-other"]', value)
    return this
  }

  getOtherEthnicGroupAnswerOther(value) {
    return browser.element('[name="other-ethnic-group-answer-other"]').getValue()
  }

}

export default new OtherEthnicGroupPage()

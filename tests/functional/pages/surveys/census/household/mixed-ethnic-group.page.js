// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MixedEthnicGroupPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('mixed-ethnic-group')
  }

  clickMixedEthnicGroupAnswerWhiteAndBlackCaribbean() {
    browser.element('[id="mixed-ethnic-group-answer-0"]').click()
    return this
  }

  clickMixedEthnicGroupAnswerWhiteAndBlackAfrican() {
    browser.element('[id="mixed-ethnic-group-answer-1"]').click()
    return this
  }

  clickMixedEthnicGroupAnswerWhiteAndAsian() {
    browser.element('[id="mixed-ethnic-group-answer-2"]').click()
    return this
  }

  clickMixedEthnicGroupAnswerOther() {
    browser.element('[id="mixed-ethnic-group-answer-3"]').click()
    return this
  }

  setMixedEthnicGroupAnswerOtherText(value) {
    browser.setValue('[id="mixed-ethnic-group-answer-other"]', value)
    return this
  }

}

export default new MixedEthnicGroupPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.794894 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MixedEthnicGroupPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('mixed-ethnic-group')
  }

  clickMixedEthnicGroupAnswerWhiteAndBlackCaribbean() {
    browser.element('[id="mixed-ethnic-group-answer-1"]').click()
    return this
  }

  clickMixedEthnicGroupAnswerWhiteAndBlackAfrican() {
    browser.element('[id="mixed-ethnic-group-answer-2"]').click()
    return this
  }

  clickMixedEthnicGroupAnswerWhiteAndAsian() {
    browser.element('[id="mixed-ethnic-group-answer-3"]').click()
    return this
  }

  clickMixedEthnicGroupAnswerOther() {
    browser.element('[id="mixed-ethnic-group-answer-4"]').click()
    return this
  }

}

export default new MixedEthnicGroupPage()

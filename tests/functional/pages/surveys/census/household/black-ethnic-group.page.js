// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class BlackEthnicGroupPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('black-ethnic-group')
  }

  clickBlackEthnicGroupAnswerAfrican() {
    browser.element('[id="black-ethnic-group-answer-0"]').click()
    return this
  }

  clickBlackEthnicGroupAnswerCaribbean() {
    browser.element('[id="black-ethnic-group-answer-1"]').click()
    return this
  }

  clickBlackEthnicGroupAnswerOther() {
    browser.element('[id="black-ethnic-group-answer-2"]').click()
    return this
  }

  setBlackEthnicGroupAnswerOtherText(value) {
    browser.setValue('[id="black-ethnic-group-answer-other"]', value)
    return this
  }

}

export default new BlackEthnicGroupPage()

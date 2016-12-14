// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.803636 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class BlackEthnicGroupPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('black-ethnic-group')
  }

  clickBlackEthnicGroupAnswerAfrican() {
    browser.element('[id="black-ethnic-group-answer-1"]').click()
    return this
  }

  clickBlackEthnicGroupAnswerCaribbean() {
    browser.element('[id="black-ethnic-group-answer-2"]').click()
    return this
  }

  clickBlackEthnicGroupAnswerOther() {
    browser.element('[id="black-ethnic-group-answer-3"]').click()
    return this
  }

}

export default new BlackEthnicGroupPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.887942 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class BlackEthnicGroupPage extends MultipleChoiceWithOtherPage {

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

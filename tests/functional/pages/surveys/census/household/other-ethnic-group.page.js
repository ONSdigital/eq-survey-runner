// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.890840 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class OtherEthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickOtherEthnicGroupAnswerArab() {
    browser.element('[id="other-ethnic-group-answer-1"]').click()
    return this
  }

  clickOtherEthnicGroupAnswerOther() {
    browser.element('[id="other-ethnic-group-answer-2"]').click()
    return this
  }

}

export default new OtherEthnicGroupPage()

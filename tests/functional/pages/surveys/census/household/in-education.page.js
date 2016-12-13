// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.862191 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class InEducationPage extends MultipleChoiceWithOtherPage {

  clickInEducationAnswerYes() {
    browser.element('[id="in-education-answer-1"]').click()
    return this
  }

  clickInEducationAnswerNo() {
    browser.element('[id="in-education-answer-2"]').click()
    return this
  }

}

export default new InEducationPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.772284 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class InEducationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('in-education')
  }

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

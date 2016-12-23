// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class InEducationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('in-education')
  }

  clickInEducationAnswerYes() {
    browser.element('[id="in-education-answer-0"]').click()
    return this
  }

  clickInEducationAnswerNo() {
    browser.element('[id="in-education-answer-1"]').click()
    return this
  }

}

export default new InEducationPage()

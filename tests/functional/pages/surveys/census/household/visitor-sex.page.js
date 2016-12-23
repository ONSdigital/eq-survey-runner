// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class VisitorSexPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('visitor-sex')
  }

  clickVisitorSexAnswerMale() {
    browser.element('[id="visitor-sex-answer-0"]').click()
    return this
  }

  clickVisitorSexAnswerFemale() {
    browser.element('[id="visitor-sex-answer-1"]').click()
    return this
  }

}

export default new VisitorSexPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.879010 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class VisitorSexPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('visitor-sex')
  }

  clickVisitorSexAnswerMale() {
    browser.element('[id="visitor-sex-answer-1"]').click()
    return this
  }

  clickVisitorSexAnswerFemale() {
    browser.element('[id="visitor-sex-answer-2"]').click()
    return this
  }

}

export default new VisitorSexPage()

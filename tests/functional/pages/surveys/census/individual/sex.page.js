// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class SexPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('sex')
  }

  clickSexAnswerMale() {
    browser.element('[id="sex-answer-0"]').click()
    return this
  }

  clickSexAnswerFemale() {
    browser.element('[id="sex-answer-1"]').click()
    return this
  }

}

export default new SexPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.760805 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class SexPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('sex')
  }

  clickSexAnswerMale() {
    browser.element('[id="sex-answer-1"]').click()
    return this
  }

  clickSexAnswerFemale() {
    browser.element('[id="sex-answer-2"]').click()
    return this
  }

}

export default new SexPage()

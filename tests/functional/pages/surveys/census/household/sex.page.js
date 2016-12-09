// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.849614 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class SexPage extends MultipleChoiceWithOtherPage {

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

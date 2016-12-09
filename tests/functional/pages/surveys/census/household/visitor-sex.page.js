// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.973307 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class VisitorSexPage extends MultipleChoiceWithOtherPage {

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

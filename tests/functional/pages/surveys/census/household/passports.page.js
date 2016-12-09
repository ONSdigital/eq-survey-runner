// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.908107 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PassportsPage extends MultipleChoiceWithOtherPage {

  clickPassportsAnswerUnitedKingdom() {
    browser.element('[id="passports-answer-1"]').click()
    return this
  }

  clickPassportsAnswerIrish() {
    browser.element('[id="passports-answer-2"]').click()
    return this
  }

  clickPassportsAnswerOther() {
    browser.element('[id="passports-answer-3"]').click()
    return this
  }

  clickPassportsAnswerNone() {
    browser.element('[id="passports-answer-4"]').click()
    return this
  }

}

export default new PassportsPage()

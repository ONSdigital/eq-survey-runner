// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingReplacingPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-replacing')
  }

  clickFactorsAffectingReplacingAnswerHigh() {
    browser.element('[id="factors-affecting-replacing-answer-0"]').click()
    return this
  }

  clickFactorsAffectingReplacingAnswerMedium() {
    browser.element('[id="factors-affecting-replacing-answer-1"]').click()
    return this
  }

  clickFactorsAffectingReplacingAnswerLow() {
    browser.element('[id="factors-affecting-replacing-answer-2"]').click()
    return this
  }

  clickFactorsAffectingReplacingAnswerNotImportant() {
    browser.element('[id="factors-affecting-replacing-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingReplacingPage()

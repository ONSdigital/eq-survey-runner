// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingValuePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-value')
  }

  clickFactorsAffectingValueAnswerHigh() {
    browser.element('[id="factors-affecting-value-answer-0"]').click()
    return this
  }

  clickFactorsAffectingValueAnswerMedium() {
    browser.element('[id="factors-affecting-value-answer-1"]').click()
    return this
  }

  clickFactorsAffectingValueAnswerLow() {
    browser.element('[id="factors-affecting-value-answer-2"]').click()
    return this
  }

  clickFactorsAffectingValueAnswerNotImportant() {
    browser.element('[id="factors-affecting-value-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingValuePage()

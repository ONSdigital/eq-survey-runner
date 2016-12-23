// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingFlexibilityPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-flexibility')
  }

  clickFactorsAffectingFlexibilityAnswerHigh() {
    browser.element('[id="factors-affecting-flexibility-answer-0"]').click()
    return this
  }

  clickFactorsAffectingFlexibilityAnswerMedium() {
    browser.element('[id="factors-affecting-flexibility-answer-1"]').click()
    return this
  }

  clickFactorsAffectingFlexibilityAnswerLow() {
    browser.element('[id="factors-affecting-flexibility-answer-2"]').click()
    return this
  }

  clickFactorsAffectingFlexibilityAnswerNotImportant() {
    browser.element('[id="factors-affecting-flexibility-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingFlexibilityPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingHealthSafetyPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-health-safety')
  }

  clickFactorsAffectingHealthSafetyAnswerHigh() {
    browser.element('[id="factors-affecting-health-safety-answer-0"]').click()
    return this
  }

  clickFactorsAffectingHealthSafetyAnswerMedium() {
    browser.element('[id="factors-affecting-health-safety-answer-1"]').click()
    return this
  }

  clickFactorsAffectingHealthSafetyAnswerLow() {
    browser.element('[id="factors-affecting-health-safety-answer-2"]').click()
    return this
  }

  clickFactorsAffectingHealthSafetyAnswerNotImportant() {
    browser.element('[id="factors-affecting-health-safety-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingHealthSafetyPage()

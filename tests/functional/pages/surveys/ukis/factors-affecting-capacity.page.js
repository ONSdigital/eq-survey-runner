// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingCapacityPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-capacity')
  }

  clickFactorsAffectingCapacityAnswerHigh() {
    browser.element('[id="factors-affecting-capacity-answer-0"]').click()
    return this
  }

  clickFactorsAffectingCapacityAnswerMedium() {
    browser.element('[id="factors-affecting-capacity-answer-1"]').click()
    return this
  }

  clickFactorsAffectingCapacityAnswerLow() {
    browser.element('[id="factors-affecting-capacity-answer-2"]').click()
    return this
  }

  clickFactorsAffectingCapacityAnswerNotImportant() {
    browser.element('[id="factors-affecting-capacity-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingCapacityPage()

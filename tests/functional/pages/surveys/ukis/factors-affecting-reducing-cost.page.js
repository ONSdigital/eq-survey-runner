// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingReducingCostPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-reducing-cost')
  }

  clickFactorsAffectingReducingCostAnswerHigh() {
    browser.element('[id="factors-affecting-reducing-cost-answer-0"]').click()
    return this
  }

  clickFactorsAffectingReducingCostAnswerMedium() {
    browser.element('[id="factors-affecting-reducing-cost-answer-1"]').click()
    return this
  }

  clickFactorsAffectingReducingCostAnswerLow() {
    browser.element('[id="factors-affecting-reducing-cost-answer-2"]').click()
    return this
  }

  clickFactorsAffectingReducingCostAnswerNotImportant() {
    browser.element('[id="factors-affecting-reducing-cost-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingReducingCostPage()

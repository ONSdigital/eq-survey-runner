// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingEnvironmentalPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-environmental')
  }

  clickFactorsAffectingEnvironmentalAnswerHigh() {
    browser.element('[id="factors-affecting-environmental-answer-0"]').click()
    return this
  }

  clickFactorsAffectingEnvironmentalAnswerMedium() {
    browser.element('[id="factors-affecting-environmental-answer-1"]').click()
    return this
  }

  clickFactorsAffectingEnvironmentalAnswerLow() {
    browser.element('[id="factors-affecting-environmental-answer-2"]').click()
    return this
  }

  clickFactorsAffectingEnvironmentalAnswerNotImportant() {
    browser.element('[id="factors-affecting-environmental-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingEnvironmentalPage()

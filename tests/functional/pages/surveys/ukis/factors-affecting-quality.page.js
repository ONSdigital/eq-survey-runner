// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingQualityPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-quality')
  }

  clickFactorsAffectingQualityAnswerHigh() {
    browser.element('[id="factors-affecting-quality-answer-0"]').click()
    return this
  }

  clickFactorsAffectingQualityAnswerMedium() {
    browser.element('[id="factors-affecting-quality-answer-1"]').click()
    return this
  }

  clickFactorsAffectingQualityAnswerLow() {
    browser.element('[id="factors-affecting-quality-answer-2"]').click()
    return this
  }

  clickFactorsAffectingQualityAnswerNotImportant() {
    browser.element('[id="factors-affecting-quality-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingQualityPage()

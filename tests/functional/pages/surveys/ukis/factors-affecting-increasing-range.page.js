// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingIncreasingRangePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-increasing-range')
  }

  clickFactorsAffectingIncreasingRangeAnswerHigh() {
    browser.element('[id="factors-affecting-increasing-range-answer-0"]').click()
    return this
  }

  clickFactorsAffectingIncreasingRangeAnswerMedium() {
    browser.element('[id="factors-affecting-increasing-range-answer-1"]').click()
    return this
  }

  clickFactorsAffectingIncreasingRangeAnswerLow() {
    browser.element('[id="factors-affecting-increasing-range-answer-2"]').click()
    return this
  }

  clickFactorsAffectingIncreasingRangeAnswerNotImportant() {
    browser.element('[id="factors-affecting-increasing-range-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingIncreasingRangePage()

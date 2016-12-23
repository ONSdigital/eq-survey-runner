// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingNewMarketsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-new-markets')
  }

  clickFactorsAffectingNewMarketsAnswerHigh() {
    browser.element('[id="factors-affecting-new-markets-answer-0"]').click()
    return this
  }

  clickFactorsAffectingNewMarketsAnswerMedium() {
    browser.element('[id="factors-affecting-new-markets-answer-1"]').click()
    return this
  }

  clickFactorsAffectingNewMarketsAnswerLow() {
    browser.element('[id="factors-affecting-new-markets-answer-2"]').click()
    return this
  }

  clickFactorsAffectingNewMarketsAnswerNotImportant() {
    browser.element('[id="factors-affecting-new-markets-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingNewMarketsPage()

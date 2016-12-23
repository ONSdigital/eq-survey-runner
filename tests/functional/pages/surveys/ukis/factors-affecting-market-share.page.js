// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingMarketSharePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-market-share')
  }

  clickFactorsAffectingMarketShareAnswerHigh() {
    browser.element('[id="factors-affecting-market-share-answer-0"]').click()
    return this
  }

  clickFactorsAffectingMarketShareAnswerMedium() {
    browser.element('[id="factors-affecting-market-share-answer-1"]').click()
    return this
  }

  clickFactorsAffectingMarketShareAnswerLow() {
    browser.element('[id="factors-affecting-market-share-answer-2"]').click()
    return this
  }

  clickFactorsAffectingMarketShareAnswerNotImportant() {
    browser.element('[id="factors-affecting-market-share-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingMarketSharePage()

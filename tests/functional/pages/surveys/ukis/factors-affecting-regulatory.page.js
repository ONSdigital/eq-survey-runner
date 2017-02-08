// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FactorsAffectingRegulatoryPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('factors-affecting-regulatory')
  }

  clickFactorsAffectingRegulatoryAnswerHigh() {
    browser.element('[id="factors-affecting-regulatory-answer-0"]').click()
    return this
  }

  clickFactorsAffectingRegulatoryAnswerMedium() {
    browser.element('[id="factors-affecting-regulatory-answer-1"]').click()
    return this
  }

  clickFactorsAffectingRegulatoryAnswerLow() {
    browser.element('[id="factors-affecting-regulatory-answer-2"]').click()
    return this
  }

  clickFactorsAffectingRegulatoryAnswerNotImportant() {
    browser.element('[id="factors-affecting-regulatory-answer-3"]').click()
    return this
  }

}

export default new FactorsAffectingRegulatoryPage()

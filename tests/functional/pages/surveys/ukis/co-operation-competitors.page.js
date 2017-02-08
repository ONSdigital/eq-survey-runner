// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CoOperationCompetitorsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('co-operation-competitors')
  }

  clickCoOperationCompetitorsAnswerUkRegional() {
    browser.element('[id="co-operation-competitors-answer-0"]').click()
    return this
  }

  clickCoOperationCompetitorsAnswerUkNational() {
    browser.element('[id="co-operation-competitors-answer-1"]').click()
    return this
  }

  clickCoOperationCompetitorsAnswerEuropeanCountries() {
    browser.element('[id="co-operation-competitors-answer-2"]').click()
    return this
  }

  clickCoOperationCompetitorsAnswerOtherCountries() {
    browser.element('[id="co-operation-competitors-answer-3"]').click()
    return this
  }

}

export default new CoOperationCompetitorsPage()

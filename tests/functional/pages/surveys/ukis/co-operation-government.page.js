// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CoOperationGovernmentPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('co-operation-government')
  }

  clickCoOperationGovernmentAnswerUkRegional() {
    browser.element('[id="co-operation-government-answer-0"]').click()
    return this
  }

  clickCoOperationGovernmentAnswerUkNational() {
    browser.element('[id="co-operation-government-answer-1"]').click()
    return this
  }

  clickCoOperationGovernmentAnswerEuropeanCountries() {
    browser.element('[id="co-operation-government-answer-2"]').click()
    return this
  }

  clickCoOperationGovernmentAnswerOtherCountries() {
    browser.element('[id="co-operation-government-answer-3"]').click()
    return this
  }

}

export default new CoOperationGovernmentPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CoOperationPrivateSectorPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('co-operation-private-sector')
  }

  clickCoOperationPrivateSectorAnswerUkRegional() {
    browser.element('[id="co-operation-private-sector-answer-0"]').click()
    return this
  }

  clickCoOperationPrivateSectorAnswerUkNational() {
    browser.element('[id="co-operation-private-sector-answer-1"]').click()
    return this
  }

  clickCoOperationPrivateSectorAnswerEuropeanCountries() {
    browser.element('[id="co-operation-private-sector-answer-2"]').click()
    return this
  }

  clickCoOperationPrivateSectorAnswerOtherCountries() {
    browser.element('[id="co-operation-private-sector-answer-3"]').click()
    return this
  }

}

export default new CoOperationPrivateSectorPage()

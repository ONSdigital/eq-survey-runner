// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CoOperationSuppliersPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('co-operation-suppliers')
  }

  clickCoOperationSuppliersAnswerUkRegional() {
    browser.element('[id="co-operation-suppliers-answer-0"]').click()
    return this
  }

  clickCoOperationSuppliersAnswerUkNational() {
    browser.element('[id="co-operation-suppliers-answer-1"]').click()
    return this
  }

  clickCoOperationSuppliersAnswerEuropeanCountries() {
    browser.element('[id="co-operation-suppliers-answer-2"]').click()
    return this
  }

  clickCoOperationSuppliersAnswerOtherCountries() {
    browser.element('[id="co-operation-suppliers-answer-3"]').click()
    return this
  }

}

export default new CoOperationSuppliersPage()

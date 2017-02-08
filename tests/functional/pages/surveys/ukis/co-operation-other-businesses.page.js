// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CoOperationOtherBusinessesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('co-operation-other-businesses')
  }

  clickCoOperationOtherBusinessesAnswerUkRegional() {
    browser.element('[id="co-operation-other-businesses-answer-0"]').click()
    return this
  }

  clickCoOperationOtherBusinessesAnswerUkNational() {
    browser.element('[id="co-operation-other-businesses-answer-1"]').click()
    return this
  }

  clickCoOperationOtherBusinessesAnswerEuropeanCountries() {
    browser.element('[id="co-operation-other-businesses-answer-2"]').click()
    return this
  }

  clickCoOperationOtherBusinessesAnswerOtherCountries() {
    browser.element('[id="co-operation-other-businesses-answer-3"]').click()
    return this
  }

}

export default new CoOperationOtherBusinessesPage()

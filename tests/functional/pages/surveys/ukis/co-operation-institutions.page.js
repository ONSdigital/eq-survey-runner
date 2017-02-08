// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CoOperationInstitutionsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('co-operation-institutions')
  }

  clickCoOperationInstitutionsAnswerUkRegional() {
    browser.element('[id="co-operation-institutions-answer-0"]').click()
    return this
  }

  clickCoOperationInstitutionsAnswerUkNational() {
    browser.element('[id="co-operation-institutions-answer-1"]').click()
    return this
  }

  clickCoOperationInstitutionsAnswerEuropeanCountries() {
    browser.element('[id="co-operation-institutions-answer-2"]').click()
    return this
  }

  clickCoOperationInstitutionsAnswerOtherCountries() {
    browser.element('[id="co-operation-institutions-answer-3"]').click()
    return this
  }

}

export default new CoOperationInstitutionsPage()

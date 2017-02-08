// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CoOperationConsultantsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('co-operation-consultants')
  }

  clickCoOperationConsultantsAnswerUkRegional() {
    browser.element('[id="co-operation-consultants-answer-0"]').click()
    return this
  }

  clickCoOperationConsultantsAnswerUkNational() {
    browser.element('[id="co-operation-consultants-answer-1"]').click()
    return this
  }

  clickCoOperationConsultantsAnswerEuropeanCountries() {
    browser.element('[id="co-operation-consultants-answer-2"]').click()
    return this
  }

  clickCoOperationConsultantsAnswerOtherCountries() {
    browser.element('[id="co-operation-consultants-answer-3"]').click()
    return this
  }

}

export default new CoOperationConsultantsPage()

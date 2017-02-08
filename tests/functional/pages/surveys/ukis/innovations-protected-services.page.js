// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InnovationsProtectedServicesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('innovations-protected-services')
  }

  clickInnovationsProtectedServicesAnswerNone() {
    browser.element('[id="innovations-protected-services-answer-0"]').click()
    return this
  }

  clickInnovationsProtectedServicesAnswerLessThan40() {
    browser.element('[id="innovations-protected-services-answer-1"]').click()
    return this
  }

  clickInnovationsProtectedServicesAnswer4090() {
    browser.element('[id="innovations-protected-services-answer-2"]').click()
    return this
  }

  clickInnovationsProtectedServicesAnswerOver90() {
    browser.element('[id="innovations-protected-services-answer-3"]').click()
    return this
  }

}

export default new InnovationsProtectedServicesPage()

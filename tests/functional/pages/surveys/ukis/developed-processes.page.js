// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class DevelopedProcessesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('developed-processes')
  }

  clickDevelopedProcessesAnswerThisBusinessOrEnterpriseGroup() {
    browser.element('[id="developed-processes-answer-0"]').click()
    return this
  }

  clickDevelopedProcessesAnswerThisBusinessWithOtherBusinessesOrOrganisations() {
    browser.element('[id="developed-processes-answer-1"]').click()
    return this
  }

  clickDevelopedProcessesAnswerOtherBusinessesOrOrganisations() {
    browser.element('[id="developed-processes-answer-2"]').click()
    return this
  }

}

export default new DevelopedProcessesPage()

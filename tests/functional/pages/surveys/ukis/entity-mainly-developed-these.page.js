// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class EntityMainlyDevelopedThesePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('entity-mainly-developed-these')
  }

  clickEntityMainlyDevelopedTheseAnswerThisBusinessOrEnterpriseGroup() {
    browser.element('[id="entity-mainly-developed-these-answer-0"]').click()
    return this
  }

  clickEntityMainlyDevelopedTheseAnswerThisBusinessWithOtherBusinessesOrOrganisations() {
    browser.element('[id="entity-mainly-developed-these-answer-1"]').click()
    return this
  }

  clickEntityMainlyDevelopedTheseAnswerOtherBusinessesOrOrganisations() {
    browser.element('[id="entity-mainly-developed-these-answer-2"]').click()
    return this
  }

}

export default new EntityMainlyDevelopedThesePage()

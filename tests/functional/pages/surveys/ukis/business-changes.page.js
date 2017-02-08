// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class BusinessChangesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('business-changes')
  }

  clickBusinessChangesBusinessPracticesAnswerYes() {
    browser.element('[id="business-changes-business-practices-answer-0"]').click()
    return this
  }

  clickBusinessChangesBusinessPracticesAnswerNo() {
    browser.element('[id="business-changes-business-practices-answer-1"]').click()
    return this
  }

  clickBusinessChangesOrganisingAnswerYes() {
    browser.element('[id="business-changes-organising-answer-0"]').click()
    return this
  }

  clickBusinessChangesOrganisingAnswerNo() {
    browser.element('[id="business-changes-organising-answer-1"]').click()
    return this
  }

  clickBusinessChangesExternalRelationshipsAnswerYes() {
    browser.element('[id="business-changes-external-relationships-answer-0"]').click()
    return this
  }

  clickBusinessChangesExternalRelationshipsAnswerNo() {
    browser.element('[id="business-changes-external-relationships-answer-1"]').click()
    return this
  }

  clickBusinessChangesAnswerYes() {
    browser.element('[id="business-changes-answer-0"]').click()
    return this
  }

  clickBusinessChangesAnswerNo() {
    browser.element('[id="business-changes-answer-1"]').click()
    return this
  }

}

export default new BusinessChangesPage()

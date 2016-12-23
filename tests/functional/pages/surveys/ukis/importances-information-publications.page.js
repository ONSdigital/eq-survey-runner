// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationPublicationsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-publications')
  }

  clickImportancesInformationPublicationsAnswerHigh() {
    browser.element('[id="importances-information-publications-answer-0"]').click()
    return this
  }

  clickImportancesInformationPublicationsAnswerMedium() {
    browser.element('[id="importances-information-publications-answer-1"]').click()
    return this
  }

  clickImportancesInformationPublicationsAnswerLow() {
    browser.element('[id="importances-information-publications-answer-2"]').click()
    return this
  }

  clickImportancesInformationPublicationsAnswerNotImportant() {
    browser.element('[id="importances-information-publications-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationPublicationsPage()

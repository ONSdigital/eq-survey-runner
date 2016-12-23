// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationAssociationsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-associations')
  }

  clickImportancesInformationAssociationsAnswerHigh() {
    browser.element('[id="importances-information-associations-answer-0"]').click()
    return this
  }

  clickImportancesInformationAssociationsAnswerMedium() {
    browser.element('[id="importances-information-associations-answer-1"]').click()
    return this
  }

  clickImportancesInformationAssociationsAnswerLow() {
    browser.element('[id="importances-information-associations-answer-2"]').click()
    return this
  }

  clickImportancesInformationAssociationsAnswerNotImportant() {
    browser.element('[id="importances-information-associations-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationAssociationsPage()

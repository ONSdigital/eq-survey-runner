// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationStandardsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-standards')
  }

  clickImportancesInformationStandardsAnswerHigh() {
    browser.element('[id="importances-information-standards-answer-0"]').click()
    return this
  }

  clickImportancesInformationStandardsAnswerMedium() {
    browser.element('[id="importances-information-standards-answer-1"]').click()
    return this
  }

  clickImportancesInformationStandardsAnswerLow() {
    browser.element('[id="importances-information-standards-answer-2"]').click()
    return this
  }

  clickImportancesInformationStandardsAnswerNotImportant() {
    browser.element('[id="importances-information-standards-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationStandardsPage()

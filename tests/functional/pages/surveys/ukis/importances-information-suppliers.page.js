// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationSuppliersPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-suppliers')
  }

  clickImportancesInformationSuppliersAnswerHigh() {
    browser.element('[id="importances-information-suppliers-answer-0"]').click()
    return this
  }

  clickImportancesInformationSuppliersAnswerMedium() {
    browser.element('[id="importances-information-suppliers-answer-1"]').click()
    return this
  }

  clickImportancesInformationSuppliersAnswerLow() {
    browser.element('[id="importances-information-suppliers-answer-2"]').click()
    return this
  }

  clickImportancesInformationSuppliersAnswerNotImportant() {
    browser.element('[id="importances-information-suppliers-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationSuppliersPage()

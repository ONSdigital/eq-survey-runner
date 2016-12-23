// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationClientPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-client')
  }

  clickImportancesInformationClientAnswerHigh() {
    browser.element('[id="importances-information-client-answer-0"]').click()
    return this
  }

  clickImportancesInformationClientAnswerMedium() {
    browser.element('[id="importances-information-client-answer-1"]').click()
    return this
  }

  clickImportancesInformationClientAnswerLow() {
    browser.element('[id="importances-information-client-answer-2"]').click()
    return this
  }

  clickImportancesInformationClientAnswerNotImportant() {
    browser.element('[id="importances-information-client-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationClientPage()

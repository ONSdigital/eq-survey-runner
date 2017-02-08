// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationConferencesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-conferences')
  }

  clickImportancesInformationConferencesAnswerHigh() {
    browser.element('[id="importances-information-conferences-answer-0"]').click()
    return this
  }

  clickImportancesInformationConferencesAnswerMedium() {
    browser.element('[id="importances-information-conferences-answer-1"]').click()
    return this
  }

  clickImportancesInformationConferencesAnswerLow() {
    browser.element('[id="importances-information-conferences-answer-2"]').click()
    return this
  }

  clickImportancesInformationConferencesAnswerNotImportant() {
    browser.element('[id="importances-information-conferences-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationConferencesPage()

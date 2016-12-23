// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationGovernmentPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-government')
  }

  clickImportancesInformationGovernmentAnswerHigh() {
    browser.element('[id="importances-information-government-answer-0"]').click()
    return this
  }

  clickImportancesInformationGovernmentAnswerMedium() {
    browser.element('[id="importances-information-government-answer-1"]').click()
    return this
  }

  clickImportancesInformationGovernmentAnswerLow() {
    browser.element('[id="importances-information-government-answer-2"]').click()
    return this
  }

  clickImportancesInformationGovernmentAnswerNotImportant() {
    browser.element('[id="importances-information-government-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationGovernmentPage()

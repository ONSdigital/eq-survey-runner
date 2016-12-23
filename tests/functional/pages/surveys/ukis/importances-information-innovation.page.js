// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationInnovationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-innovation')
  }

  clickImportancesInformationInnovationAnswerHigh() {
    browser.element('[id="importances-information-innovation-answer-0"]').click()
    return this
  }

  clickImportancesInformationInnovationAnswerMedium() {
    browser.element('[id="importances-information-innovation-answer-1"]').click()
    return this
  }

  clickImportancesInformationInnovationAnswerLow() {
    browser.element('[id="importances-information-innovation-answer-2"]').click()
    return this
  }

  clickImportancesInformationInnovationAnswerNotImportant() {
    browser.element('[id="importances-information-innovation-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationInnovationPage()

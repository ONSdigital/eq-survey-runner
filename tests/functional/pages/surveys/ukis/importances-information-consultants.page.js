// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationConsultantsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-consultants')
  }

  clickImportancesInformationConsultantsAnswerHigh() {
    browser.element('[id="importances-information-consultants-answer-0"]').click()
    return this
  }

  clickImportancesInformationConsultantsAnswerMedium() {
    browser.element('[id="importances-information-consultants-answer-1"]').click()
    return this
  }

  clickImportancesInformationConsultantsAnswerLow() {
    browser.element('[id="importances-information-consultants-answer-2"]').click()
    return this
  }

  clickImportancesInformationConsultantsAnswerNotImportant() {
    browser.element('[id="importances-information-consultants-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationConsultantsPage()

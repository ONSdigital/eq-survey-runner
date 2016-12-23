// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationUniversitiesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-universities')
  }

  clickImportancesInformationUniversitiesAnswerHigh() {
    browser.element('[id="importances-information-universities-answer-0"]').click()
    return this
  }

  clickImportancesInformationUniversitiesAnswerMedium() {
    browser.element('[id="importances-information-universities-answer-1"]').click()
    return this
  }

  clickImportancesInformationUniversitiesAnswerLow() {
    browser.element('[id="importances-information-universities-answer-2"]').click()
    return this
  }

  clickImportancesInformationUniversitiesAnswerNotImportant() {
    browser.element('[id="importances-information-universities-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationUniversitiesPage()

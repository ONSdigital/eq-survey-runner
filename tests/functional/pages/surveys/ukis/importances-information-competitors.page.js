// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationCompetitorsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-competitors')
  }

  clickImportancesInformationCompetitorsAnswerHigh() {
    browser.element('[id="importances-information-competitors-answer-0"]').click()
    return this
  }

  clickImportancesInformationCompetitorsAnswerMedium() {
    browser.element('[id="importances-information-competitors-answer-1"]').click()
    return this
  }

  clickImportancesInformationCompetitorsAnswerLow() {
    browser.element('[id="importances-information-competitors-answer-2"]').click()
    return this
  }

  clickImportancesInformationCompetitorsAnswerNotImportant() {
    browser.element('[id="importances-information-competitors-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationCompetitorsPage()

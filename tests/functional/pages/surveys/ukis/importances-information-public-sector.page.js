// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ImportancesInformationPublicSectorPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('importances-information-public-sector')
  }

  clickImportancesInformationPublicSectorAnswerHigh() {
    browser.element('[id="importances-information-public-sector-answer-0"]').click()
    return this
  }

  clickImportancesInformationPublicSectorAnswerMedium() {
    browser.element('[id="importances-information-public-sector-answer-1"]').click()
    return this
  }

  clickImportancesInformationPublicSectorAnswerLow() {
    browser.element('[id="importances-information-public-sector-answer-2"]').click()
    return this
  }

  clickImportancesInformationPublicSectorAnswerNotImportant() {
    browser.element('[id="importances-information-public-sector-answer-3"]').click()
    return this
  }

}

export default new ImportancesInformationPublicSectorPage()

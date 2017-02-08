// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CoOperationPublicSectorPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('co-operation-public-sector')
  }

  clickCoOperationPublicSectorAnswerUkRegional() {
    browser.element('[id="co-operation-public-sector-answer-0"]').click()
    return this
  }

  clickCoOperationPublicSectorAnswerUkNational() {
    browser.element('[id="co-operation-public-sector-answer-1"]').click()
    return this
  }

  clickCoOperationPublicSectorAnswerEuropeanCountries() {
    browser.element('[id="co-operation-public-sector-answer-2"]').click()
    return this
  }

  clickCoOperationPublicSectorAnswerOtherCountries() {
    browser.element('[id="co-operation-public-sector-answer-3"]').click()
    return this
  }

}

export default new CoOperationPublicSectorPage()

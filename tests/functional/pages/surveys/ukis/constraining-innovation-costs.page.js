// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ConstrainingInnovationCostsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('constraining-innovation-costs')
  }

  clickConstrainingInnovationCostsAnswerHigh() {
    browser.element('[id="constraining-innovation-costs-answer-0"]').click()
    return this
  }

  clickConstrainingInnovationCostsAnswerMedium() {
    browser.element('[id="constraining-innovation-costs-answer-1"]').click()
    return this
  }

  clickConstrainingInnovationCostsAnswerLow() {
    browser.element('[id="constraining-innovation-costs-answer-2"]').click()
    return this
  }

  clickConstrainingInnovationCostsAnswerNotImportant() {
    browser.element('[id="constraining-innovation-costs-answer-3"]').click()
    return this
  }

}

export default new ConstrainingInnovationCostsPage()

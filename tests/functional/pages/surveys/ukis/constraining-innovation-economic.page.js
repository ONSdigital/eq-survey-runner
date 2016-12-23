// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ConstrainingInnovationEconomicPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('constraining-innovation-economic')
  }

  clickConstrainingInnovationEconomicAnswerHigh() {
    browser.element('[id="constraining-innovation-economic-answer-0"]').click()
    return this
  }

  clickConstrainingInnovationEconomicAnswerMedium() {
    browser.element('[id="constraining-innovation-economic-answer-1"]').click()
    return this
  }

  clickConstrainingInnovationEconomicAnswerLow() {
    browser.element('[id="constraining-innovation-economic-answer-2"]').click()
    return this
  }

  clickConstrainingInnovationEconomicAnswerNotImportant() {
    browser.element('[id="constraining-innovation-economic-answer-3"]').click()
    return this
  }

}

export default new ConstrainingInnovationEconomicPage()

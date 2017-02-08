// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ConstrainingInnovationGovernmentPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('constraining-innovation-government')
  }

  clickConstrainingInnovationGovernmentAnswerHigh() {
    browser.element('[id="constraining-innovation-government-answer-0"]').click()
    return this
  }

  clickConstrainingInnovationGovernmentAnswerMedium() {
    browser.element('[id="constraining-innovation-government-answer-1"]').click()
    return this
  }

  clickConstrainingInnovationGovernmentAnswerLow() {
    browser.element('[id="constraining-innovation-government-answer-2"]').click()
    return this
  }

  clickConstrainingInnovationGovernmentAnswerNotImportant() {
    browser.element('[id="constraining-innovation-government-answer-3"]').click()
    return this
  }

}

export default new ConstrainingInnovationGovernmentPage()

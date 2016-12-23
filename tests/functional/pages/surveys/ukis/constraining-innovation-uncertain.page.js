// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ConstrainingInnovationUncertainPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('constraining-innovation-uncertain')
  }

  clickConstrainingInnovationUncertainAnswerHigh() {
    browser.element('[id="constraining-innovation-uncertain-answer-0"]').click()
    return this
  }

  clickConstrainingInnovationUncertainAnswerMedium() {
    browser.element('[id="constraining-innovation-uncertain-answer-1"]').click()
    return this
  }

  clickConstrainingInnovationUncertainAnswerLow() {
    browser.element('[id="constraining-innovation-uncertain-answer-2"]').click()
    return this
  }

  clickConstrainingInnovationUncertainAnswerNotImportant() {
    browser.element('[id="constraining-innovation-uncertain-answer-3"]').click()
    return this
  }

}

export default new ConstrainingInnovationUncertainPage()

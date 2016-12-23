// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ConstrainingInnovationDominatedPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('constraining-innovation-dominated')
  }

  clickConstrainingInnovationDominatedAnswerHigh() {
    browser.element('[id="constraining-innovation-dominated-answer-0"]').click()
    return this
  }

  clickConstrainingInnovationDominatedAnswerMedium() {
    browser.element('[id="constraining-innovation-dominated-answer-1"]').click()
    return this
  }

  clickConstrainingInnovationDominatedAnswerLow() {
    browser.element('[id="constraining-innovation-dominated-answer-2"]').click()
    return this
  }

  clickConstrainingInnovationDominatedAnswerNotImportant() {
    browser.element('[id="constraining-innovation-dominated-answer-3"]').click()
    return this
  }

}

export default new ConstrainingInnovationDominatedPage()

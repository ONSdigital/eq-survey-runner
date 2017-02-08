// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ConstrainingInnovationReferendumPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('constraining-innovation-referendum')
  }

  clickConstrainingInnovationReferendumAnswerHigh() {
    browser.element('[id="constraining-innovation-referendum-answer-0"]').click()
    return this
  }

  clickConstrainingInnovationReferendumAnswerMedium() {
    browser.element('[id="constraining-innovation-referendum-answer-1"]').click()
    return this
  }

  clickConstrainingInnovationReferendumAnswerLow() {
    browser.element('[id="constraining-innovation-referendum-answer-2"]').click()
    return this
  }

  clickConstrainingInnovationReferendumAnswerNotImportant() {
    browser.element('[id="constraining-innovation-referendum-answer-3"]').click()
    return this
  }

}

export default new ConstrainingInnovationReferendumPage()

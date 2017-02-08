// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ConstrainingInnovationEuPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('constraining-innovation-eu')
  }

  clickConstrainingInnovationEuAnswerHigh() {
    browser.element('[id="constraining-innovation-eu-answer-0"]').click()
    return this
  }

  clickConstrainingInnovationEuAnswerMedium() {
    browser.element('[id="constraining-innovation-eu-answer-1"]').click()
    return this
  }

  clickConstrainingInnovationEuAnswerLow() {
    browser.element('[id="constraining-innovation-eu-answer-2"]').click()
    return this
  }

  clickConstrainingInnovationEuAnswerNotImportant() {
    browser.element('[id="constraining-innovation-eu-answer-3"]').click()
    return this
  }

}

export default new ConstrainingInnovationEuPage()

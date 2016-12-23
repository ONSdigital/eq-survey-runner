// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ConstrainingInnovationLackInformationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('constraining-innovation-lack-information')
  }

  clickConstrainingInnovationLackInformationAnswerHigh() {
    browser.element('[id="constraining-innovation-lack-information-answer-0"]').click()
    return this
  }

  clickConstrainingInnovationLackInformationAnswerMedium() {
    browser.element('[id="constraining-innovation-lack-information-answer-1"]').click()
    return this
  }

  clickConstrainingInnovationLackInformationAnswerLow() {
    browser.element('[id="constraining-innovation-lack-information-answer-2"]').click()
    return this
  }

  clickConstrainingInnovationLackInformationAnswerNotImportant() {
    browser.element('[id="constraining-innovation-lack-information-answer-3"]').click()
    return this
  }

}

export default new ConstrainingInnovationLackInformationPage()

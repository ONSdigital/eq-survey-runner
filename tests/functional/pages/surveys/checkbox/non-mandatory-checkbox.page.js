// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class NonMandatoryCheckboxPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('non-mandatory-checkbox')
  }

  clickNonMandatoryCheckboxAnswerCheese() {
    browser.element('[id="non-mandatory-checkbox-answer-0"]').click()
    return this
  }

  clickNonMandatoryCheckboxAnswerHam() {
    browser.element('[id="non-mandatory-checkbox-answer-1"]').click()
    return this
  }

  clickNonMandatoryCheckboxAnswerPineapple() {
    browser.element('[id="non-mandatory-checkbox-answer-2"]').click()
    return this
  }

  clickNonMandatoryCheckboxAnswerTuna() {
    browser.element('[id="non-mandatory-checkbox-answer-3"]').click()
    return this
  }

  clickNonMandatoryCheckboxAnswerPepperoni() {
    browser.element('[id="non-mandatory-checkbox-answer-4"]').click()
    return this
  }

  clickNonMandatoryCheckboxAnswerOther() {
    browser.element('[id="non-mandatory-checkbox-answer-5"]').click()
    return this
  }

  setNonMandatoryCheckboxAnswerOtherText(value) {
    browser.setValue('[id="other-answer-non-mandatory"]', value)
    return this
  }

}

export default new NonMandatoryCheckboxPage()

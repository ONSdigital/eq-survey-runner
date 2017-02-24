// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class MandatoryCheckboxPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('mandatory-checkbox')
  }

  clickMandatoryCheckboxAnswerCheese() {
    browser.element('[id="mandatory-checkbox-answer-0"]').click()
    return this
  }

  clickMandatoryCheckboxAnswerHam() {
    browser.element('[id="mandatory-checkbox-answer-1"]').click()
    return this
  }

  clickMandatoryCheckboxAnswerPineapple() {
    browser.element('[id="mandatory-checkbox-answer-2"]').click()
    return this
  }

  clickMandatoryCheckboxAnswerTuna() {
    browser.element('[id="mandatory-checkbox-answer-3"]').click()
    return this
  }

  clickMandatoryCheckboxAnswerPepperoni() {
    browser.element('[id="mandatory-checkbox-answer-4"]').click()
    return this
  }

  clickMandatoryCheckboxAnswerOther() {
    browser.element('[id="mandatory-checkbox-answer-5"]').click()
    return this
  }

  setMandatoryCheckboxAnswerOtherText(value) {
    browser.setValue('[id="other-answer-mandatory"]', value)
    return this
  }

}

export default new MandatoryCheckboxPage()

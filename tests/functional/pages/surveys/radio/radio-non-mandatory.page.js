// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class RadioNonMandatoryPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('radio-non-mandatory')
  }

  clickRadioNonMandatoryAnswerNone() {
    browser.element('[id="radio-non-mandatory-answer-0"]').click()
    return this
  }

  RadioNonMandatoryAnswerNoneIsSelected() {
    return browser.element('[id="radio-non-mandatory-answer-0"]').isSelected()
  }

  clickRadioNonMandatoryAnswerToast() {
    browser.element('[id="radio-non-mandatory-answer-1"]').click()
    return this
  }

  RadioNonMandatoryAnswerToastIsSelected() {
    return browser.element('[id="radio-non-mandatory-answer-1"]').isSelected()
  }

  clickRadioNonMandatoryAnswerCoffee() {
    browser.element('[id="radio-non-mandatory-answer-2"]').click()
    return this
  }

  RadioNonMandatoryAnswerCoffeeIsSelected() {
    return browser.element('[id="radio-non-mandatory-answer-2"]').isSelected()
  }

  clickRadioNonMandatoryAnswerTea() {
    browser.element('[id="radio-non-mandatory-answer-3"]').click()
    return this
  }

  RadioNonMandatoryAnswerTeaIsSelected() {
    return browser.element('[id="radio-non-mandatory-answer-3"]').isSelected()
  }

  clickRadioNonMandatoryAnswerOther() {
    browser.element('[id="radio-non-mandatory-answer-4"]').click()
    return this
  }

  RadioNonMandatoryAnswerOtherIsSelected() {
    return browser.element('[id="radio-non-mandatory-answer-4"]').isSelected()
  }

  setRadioNonMandatoryAnswerOtherText(value) {
    browser.setValue('[id="other-answer-non-mandatory"]', value)
    return this
  }

}

export default new RadioNonMandatoryPage()

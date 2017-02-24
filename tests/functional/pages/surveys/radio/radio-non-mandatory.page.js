// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class RadioNonMandatoryPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('radio-non-mandatory')
  }

  clickRadioNonMandatoryAnswerToast() {
    browser.element('[id="radio-non-mandatory-answer-0"]').click()
    return this
  }

  clickRadioNonMandatoryAnswerCoffee() {
    browser.element('[id="radio-non-mandatory-answer-1"]').click()
    return this
  }

  clickRadioNonMandatoryAnswerTea() {
    browser.element('[id="radio-non-mandatory-answer-2"]').click()
    return this
  }

  clickRadioNonMandatoryAnswerOther() {
    browser.element('[id="radio-non-mandatory-answer-3"]').click()
    return this
  }

  setRadioNonMandatoryAnswerOtherText(value) {
    browser.setValue('[id="other-answer-non-mandatory"]', value)
    return this
  }

}

export default new RadioNonMandatoryPage()

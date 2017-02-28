// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class RadioMandatoryPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('radio-mandatory')
  }

  clickRadioMandatoryAnswerBacon() {
    browser.element('[id="radio-mandatory-answer-0"]').click()
    return this
  }

  clickRadioMandatoryAnswerEggs() {
    browser.element('[id="radio-mandatory-answer-1"]').click()
    return this
  }

  clickRadioMandatoryAnswerSausage() {
    browser.element('[id="radio-mandatory-answer-2"]').click()
    return this
  }

  clickRadioMandatoryAnswerOther() {
    browser.element('[id="radio-mandatory-answer-3"]').click()
    return this
  }

  setRadioMandatoryAnswerOtherText(value) {
    browser.setValue('[id="other-answer-mandatory"]', value)
    return this
  }

}

export default new RadioMandatoryPage()

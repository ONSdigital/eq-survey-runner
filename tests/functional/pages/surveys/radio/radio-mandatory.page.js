// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class RadioMandatoryPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('radio-mandatory')
  }

  clickRadioMandatoryAnswerNone() {
    browser.element('[id="radio-mandatory-answer-0"]').click()
    return this
  }

  RadioMandatoryAnswerNoneIsSelected() {
    return browser.element('[id="radio-mandatory-answer-0"]').isSelected()
  }

  clickRadioMandatoryAnswerBacon() {
    browser.element('[id="radio-mandatory-answer-1"]').click()
    return this
  }

  RadioMandatoryAnswerBaconIsSelected() {
    return browser.element('[id="radio-mandatory-answer-1"]').isSelected()
  }

  clickRadioMandatoryAnswerEggs() {
    browser.element('[id="radio-mandatory-answer-2"]').click()
    return this
  }

  RadioMandatoryAnswerEggsIsSelected() {
    return browser.element('[id="radio-mandatory-answer-2"]').isSelected()
  }

  clickRadioMandatoryAnswerSausage() {
    browser.element('[id="radio-mandatory-answer-3"]').click()
    return this
  }

  RadioMandatoryAnswerSausageIsSelected() {
    return browser.element('[id="radio-mandatory-answer-3"]').isSelected()
  }

  clickRadioMandatoryAnswerOther() {
    browser.element('[id="radio-mandatory-answer-4"]').click()
    return this
  }

  RadioMandatoryAnswerOtherIsSelected() {
    return browser.element('[id="radio-mandatory-answer-4"]').isSelected()
  }

  setRadioMandatoryAnswerOtherText(value) {
    browser.setValue('[id="other-answer-mandatory"]', value)
    return this
  }

}

export default new RadioMandatoryPage()

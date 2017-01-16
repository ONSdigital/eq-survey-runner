// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CountryOfBirthPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('country-of-birth')
  }

  clickCountryOfBirthEnglandAnswerEngland() {
    browser.element('[id="country-of-birth-england-answer-0"]').click()
    return this
  }

  clickCountryOfBirthEnglandAnswerWales() {
    browser.element('[id="country-of-birth-england-answer-1"]').click()
    return this
  }

  clickCountryOfBirthEnglandAnswerScotland() {
    browser.element('[id="country-of-birth-england-answer-2"]').click()
    return this
  }

  clickCountryOfBirthEnglandAnswerNorthernIreland() {
    browser.element('[id="country-of-birth-england-answer-3"]').click()
    return this
  }

  clickCountryOfBirthEnglandAnswerRepublicOfIreland() {
    browser.element('[id="country-of-birth-england-answer-4"]').click()
    return this
  }

  clickCountryOfBirthEnglandAnswerOther() {
    browser.element('[id="country-of-birth-england-answer-5"]').click()
    return this
  }

  setCountryOfBirthEnglandAnswerOther(value) {
    browser.setValue('[name="country-of-birth-england-answer-other"]', value)
    return this
  }

  getCountryOfBirthEnglandAnswerOther(value) {
    return browser.element('[name="country-of-birth-england-answer-other"]').getValue()
  }

  clickCountryOfBirthWalesAnswerWales() {
    browser.element('[id="country-of-birth-wales-answer-0"]').click()
    return this
  }

  clickCountryOfBirthWalesAnswerEngland() {
    browser.element('[id="country-of-birth-wales-answer-1"]').click()
    return this
  }

  clickCountryOfBirthWalesAnswerScotland() {
    browser.element('[id="country-of-birth-wales-answer-2"]').click()
    return this
  }

  clickCountryOfBirthWalesAnswerNorthernIreland() {
    browser.element('[id="country-of-birth-wales-answer-3"]').click()
    return this
  }

  clickCountryOfBirthWalesAnswerRepublicOfIreland() {
    browser.element('[id="country-of-birth-wales-answer-4"]').click()
    return this
  }

  clickCountryOfBirthWalesAnswerOther() {
    browser.element('[id="country-of-birth-wales-answer-5"]').click()
    return this
  }

  setCountryOfBirthWalesAnswerOther(value) {
    browser.setValue('[name="country-of-birth-wales-answer-other"]', value)
    return this
  }

  getCountryOfBirthWalesAnswerOther(value) {
    return browser.element('[name="country-of-birth-wales-answer-other"]').getValue()
  }

}

export default new CountryOfBirthPage()

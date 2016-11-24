import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CountryOfBirthPage extends MultipleChoiceWithOtherPage {

  clickEngland() {
    browser.element('[id="country-of-birth-england-answer-1"]').click()
    return this
  }

  clickWales() {
    browser.element('[id="country-of-birth-england-answer-2"]').click()
    return this
  }

  clickScotland() {
    browser.element('[id="country-of-birth-england-answer-3"]').click()
    return this
  }

  clickNorthernIreland() {
    browser.element('[id="country-of-birth-england-answer-4"]').click()
    return this
  }

  clickRepublicOfIreland() {
    browser.element('[id="country-of-birth-england-answer-5"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="country-of-birth-england-answer-6"]').click()
    return this
  }

  clickWales() {
    browser.element('[id="country-of-birth-wales-answer-1"]').click()
    return this
  }

  clickEngland() {
    browser.element('[id="country-of-birth-wales-answer-2"]').click()
    return this
  }

  clickScotland() {
    browser.element('[id="country-of-birth-wales-answer-3"]').click()
    return this
  }

  clickNorthernIreland() {
    browser.element('[id="country-of-birth-wales-answer-4"]').click()
    return this
  }

  clickRepublicOfIreland() {
    browser.element('[id="country-of-birth-wales-answer-5"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="country-of-birth-wales-answer-6"]').click()
    return this
  }

}

export default new CountryOfBirthPage()

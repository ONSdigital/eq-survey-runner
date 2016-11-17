import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AddressTypePage extends MultipleChoiceWithOtherPage {

  clickArmedForcesBaseAddress() {
    browser.element('[id="address-type-answer-1"]').click()
    return this
  }

  clickAnotherAddressWhenWorkingAwayFromHome() {
    browser.element('[id="address-type-answer-2"]').click()
    return this
  }

  clickStudentSHomeAddress() {
    browser.element('[id="address-type-answer-3"]').click()
    return this
  }

  clickStudentSTermTimeAddress() {
    browser.element('[id="address-type-answer-4"]').click()
    return this
  }

  clickAnotherParentOrGuardianSAddress() {
    browser.element('[id="address-type-answer-5"]').click()
    return this
  }

  clickHolidayHome() {
    browser.element('[id="address-type-answer-6"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="address-type-answer-7"]').click()
    return this
  }

  setAddressTypeAnswer(value) {
    browser.setValue('[name="address-type-answer"]', value)
    return this
  }

  getAddressTypeAnswer(value) {
    return browser.element('[name="address-type-answer"]').getValue()
  }

}

export default new AddressTypePage()

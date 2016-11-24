import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AddressTypePage extends MultipleChoiceWithOtherPage {

  clickAddressTypeAnswerArmedForcesBaseAddress() {
    browser.element('[id="address-type-answer-1"]').click()
    return this
  }

  clickAddressTypeAnswerAnotherAddressWhenWorkingAwayFromHome() {
    browser.element('[id="address-type-answer-2"]').click()
    return this
  }

  clickAddressTypeAnswerStudentSHomeAddress() {
    browser.element('[id="address-type-answer-3"]').click()
    return this
  }

  clickAddressTypeAnswerStudentSTermTimeAddress() {
    browser.element('[id="address-type-answer-4"]').click()
    return this
  }

  clickAddressTypeAnswerAnotherParentOrGuardianSAddress() {
    browser.element('[id="address-type-answer-5"]').click()
    return this
  }

  clickAddressTypeAnswerHolidayHome() {
    browser.element('[id="address-type-answer-6"]').click()
    return this
  }

  clickAddressTypeAnswerOther() {
    browser.element('[id="address-type-answer-7"]').click()
    return this
  }

}

export default new AddressTypePage()

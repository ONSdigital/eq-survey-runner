// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.770297 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AddressTypePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('address-type')
  }

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

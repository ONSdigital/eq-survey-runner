// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PastUsualAddressPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('past-usual-address')
  }

  clickPastUsualAddressAnswerThisAddress() {
    browser.element('[id="past-usual-address-answer-0"]').click()
    return this
  }

  clickPastUsualAddressAnswerStudentTermTimeOrBoardingSchoolAddressInTheUk() {
    browser.element('[id="past-usual-address-answer-1"]').click()
    return this
  }

  clickPastUsualAddressAnswerAnotherAddressInTheUk() {
    browser.element('[id="past-usual-address-answer-2"]').click()
    return this
  }

  clickPastUsualAddressAnswerOther() {
    browser.element('[id="past-usual-address-answer-3"]').click()
    return this
  }

  setPastUsualAddressAnswerOtherText(value) {
    browser.setValue('[id="past-usual-address-answer-other"]', value)
    return this
  }

}

export default new PastUsualAddressPage()

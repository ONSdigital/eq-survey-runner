// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.820960 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PastUsualAddressPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('past-usual-address')
  }

  clickPastUsualAddressAnswerThisAddress() {
    browser.element('[id="past-usual-address-answer-1"]').click()
    return this
  }

  clickPastUsualAddressAnswerStudentTermTimeOrBoardingSchoolAddressInTheUk() {
    browser.element('[id="past-usual-address-answer-2"]').click()
    return this
  }

  clickPastUsualAddressAnswerAnotherAddressInTheUk() {
    browser.element('[id="past-usual-address-answer-3"]').click()
    return this
  }

  clickPastUsualAddressAnswerOther() {
    browser.element('[id="past-usual-address-answer-4"]').click()
    return this
  }

}

export default new PastUsualAddressPage()

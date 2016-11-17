import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PastUsualAddressPage extends MultipleChoiceWithOtherPage {

  clickThisAddress() {
    browser.element('[id="past-usual-address-answer-1"]').click()
    return this
  }

  clickStudentTermTimeOrBoardingSchoolAddressInTheUk() {
    browser.element('[id="past-usual-address-answer-2"]').click()
    return this
  }

  clickAnotherAddressInTheUk() {
    browser.element('[id="past-usual-address-answer-3"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="past-usual-address-answer-4"]').click()
    return this
  }

  setPastUsualAddressAnswer(value) {
    browser.setValue('[name="past-usual-address-answer"]', value)
    return this
  }

  getPastUsualAddressAnswer(value) {
    return browser.element('[name="past-usual-address-answer"]').getValue()
  }

}

export default new PastUsualAddressPage()

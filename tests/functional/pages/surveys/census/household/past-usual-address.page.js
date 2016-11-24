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

}

export default new PastUsualAddressPage()

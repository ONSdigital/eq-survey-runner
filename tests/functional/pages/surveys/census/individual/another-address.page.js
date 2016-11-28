import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AnotherAddressPage extends MultipleChoiceWithOtherPage {

  clickAnotherAddressAnswerNo() {
    browser.element('[id="another-address-answer-1"]').click()
    return this
  }

  clickAnotherAddressAnswerYesAnAddressWithinTheUk() {
    browser.element('[id="another-address-answer-2"]').click()
    return this
  }

  clickAnotherAddressAnswerOther() {
    browser.element('[id="another-address-answer-3"]').click()
    return this
  }

}

export default new AnotherAddressPage()

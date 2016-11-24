import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AnotherAddressPage extends MultipleChoiceWithOtherPage {

  clickNo() {
    browser.element('[id="another-address-answer-1"]').click()
    return this
  }

  clickYesAnAddressWithinTheUk() {
    browser.element('[id="another-address-answer-2"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="another-address-answer-3"]').click()
    return this
  }

}

export default new AnotherAddressPage()

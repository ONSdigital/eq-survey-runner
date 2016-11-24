import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class DisabilityPage extends MultipleChoiceWithOtherPage {

  clickYesLimitedALot() {
    browser.element('[id="disability-answer-1"]').click()
    return this
  }

  clickYesLimitedALittle() {
    browser.element('[id="disability-answer-2"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="disability-answer-3"]').click()
    return this
  }

}

export default new DisabilityPage()

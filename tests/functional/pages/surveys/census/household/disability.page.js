import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class DisabilityPage extends MultipleChoiceWithOtherPage {

  clickDisabilityAnswerYesLimitedALot() {
    browser.element('[id="disability-answer-1"]').click()
    return this
  }

  clickDisabilityAnswerYesLimitedALittle() {
    browser.element('[id="disability-answer-2"]').click()
    return this
  }

  clickDisabilityAnswerNo() {
    browser.element('[id="disability-answer-3"]').click()
    return this
  }

}

export default new DisabilityPage()

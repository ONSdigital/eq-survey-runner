import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class OccupationPage extends MultipleChoiceWithOtherPage {

  clickOccupationAnswerRetiredWhetherReceivingAPensionOrNot() {
    browser.element('[id="occupation-answer-1"]').click()
    return this
  }

  clickOccupationAnswerAStudent() {
    browser.element('[id="occupation-answer-2"]').click()
    return this
  }

  clickOccupationAnswerLookingAfterHomeOrFamily() {
    browser.element('[id="occupation-answer-3"]').click()
    return this
  }

  clickOccupationAnswerLongTermSickOrDisabled() {
    browser.element('[id="occupation-answer-4"]').click()
    return this
  }

  clickOccupationAnswerOther() {
    browser.element('[id="occupation-answer-5"]').click()
    return this
  }

}

export default new OccupationPage()

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class OccupationPage extends MultipleChoiceWithOtherPage {

  clickRetiredWhetherReceivingAPensionOrNot() {
    browser.element('[id="occupation-answer-1"]').click()
    return this
  }

  clickAStudent() {
    browser.element('[id="occupation-answer-2"]').click()
    return this
  }

  clickLookingAfterHomeOrFamily() {
    browser.element('[id="occupation-answer-3"]').click()
    return this
  }

  clickLongTermSickOrDisabled() {
    browser.element('[id="occupation-answer-4"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="occupation-answer-5"]').click()
    return this
  }

}

export default new OccupationPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.854411 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class OccupationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('occupation')
  }

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

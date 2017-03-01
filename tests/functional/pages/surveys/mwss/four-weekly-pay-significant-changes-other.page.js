// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FourWeeklyPaySignificantChangesOtherPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('four-weekly-pay-significant-changes-other')
  }

  clickFourWeeklyPaySignificantChangesOtherAnswerYes() {
    browser.element('[id="four-weekly-pay-significant-changes-other-answer-0"]').click()
    return this
  }

  clickFourWeeklyPaySignificantChangesOtherAnswerNo() {
    browser.element('[id="four-weekly-pay-significant-changes-other-answer-1"]').click()
    return this
  }

}

export default new FourWeeklyPaySignificantChangesOtherPage()

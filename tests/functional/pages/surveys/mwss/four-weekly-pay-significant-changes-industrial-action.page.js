// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FourWeeklyPaySignificantChangesIndustrialActionPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('four-weekly-pay-significant-changes-industrial-action')
  }

  clickFourWeeklyPaySignificantChangesIndustrialActionAnswerYes() {
    browser.element('[id="four-weekly-pay-significant-changes-industrial-action-answer-0"]').click()
    return this
  }

  clickFourWeeklyPaySignificantChangesIndustrialActionAnswerNo() {
    browser.element('[id="four-weekly-pay-significant-changes-industrial-action-answer-1"]').click()
    return this
  }

}

export default new FourWeeklyPaySignificantChangesIndustrialActionPage()

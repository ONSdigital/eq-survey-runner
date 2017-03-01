// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class WeeklyPaySignificantChangesIndustrialActionPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('weekly-pay-significant-changes-industrial-action')
  }

  clickWeeklyPaySignificantChangesIndustrialActionAnswerYes() {
    browser.element('[id="weekly-pay-significant-changes-industrial-action-answer-0"]').click()
    return this
  }

  clickWeeklyPaySignificantChangesIndustrialActionAnswerNo() {
    browser.element('[id="weekly-pay-significant-changes-industrial-action-answer-1"]').click()
    return this
  }

}

export default new WeeklyPaySignificantChangesIndustrialActionPage()

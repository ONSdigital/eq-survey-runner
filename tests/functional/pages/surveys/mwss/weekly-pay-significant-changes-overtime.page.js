// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class WeeklyPaySignificantChangesOvertimePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('weekly-pay-significant-changes-overtime')
  }

  clickWeeklyPaySignificantChangesOvertimeAnswerMoreOvertime() {
    browser.element('[id="weekly-pay-significant-changes-overtime-answer-0"]').click()
    return this
  }

  clickWeeklyPaySignificantChangesOvertimeAnswerLessOvertime() {
    browser.element('[id="weekly-pay-significant-changes-overtime-answer-1"]').click()
    return this
  }

  clickWeeklyPaySignificantChangesOvertimeAnswerNoSignificantChange() {
    browser.element('[id="weekly-pay-significant-changes-overtime-answer-2"]').click()
    return this
  }

}

export default new WeeklyPaySignificantChangesOvertimePage()

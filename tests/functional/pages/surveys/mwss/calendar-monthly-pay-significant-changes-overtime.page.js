// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CalendarMonthlyPaySignificantChangesOvertimePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('calendar-monthly-pay-significant-changes-overtime')
  }

  clickCalendarMonthlyPaySignificantChangesOvertimeAnswerMoreOvertime() {
    browser.element('[id="calendar-monthly-pay-significant-changes-overtime-answer-0"]').click()
    return this
  }

  clickCalendarMonthlyPaySignificantChangesOvertimeAnswerLessOvertime() {
    browser.element('[id="calendar-monthly-pay-significant-changes-overtime-answer-1"]').click()
    return this
  }

  clickCalendarMonthlyPaySignificantChangesOvertimeAnswerNoSignificantChange() {
    browser.element('[id="calendar-monthly-pay-significant-changes-overtime-answer-2"]').click()
    return this
  }

}

export default new CalendarMonthlyPaySignificantChangesOvertimePage()

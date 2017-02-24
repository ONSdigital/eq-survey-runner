// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CalendarMonthlyPaySignificantChangesIndustrialActionPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('calendar-monthly-pay-significant-changes-industrial-action')
  }

  clickCalendarMonthlyPaySignificantChangesIndustrialActionAnswerYes() {
    browser.element('[id="calendar-monthly-pay-significant-changes-industrial-action-answer-0"]').click()
    return this
  }

  clickCalendarMonthlyPaySignificantChangesIndustrialActionAnswerNo() {
    browser.element('[id="calendar-monthly-pay-significant-changes-industrial-action-answer-1"]').click()
    return this
  }

}

export default new CalendarMonthlyPaySignificantChangesIndustrialActionPage()

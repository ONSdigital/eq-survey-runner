// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CalendarMonthlyPaySignificantChangesRedundanciesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('calendar-monthly-pay-significant-changes-redundancies')
  }

  clickCalendarMonthlyPaySignificantChangesRedundanciesAnswerYes() {
    browser.element('[id="calendar-monthly-pay-significant-changes-redundancies-answer-0"]').click()
    return this
  }

  clickCalendarMonthlyPaySignificantChangesRedundanciesAnswerNo() {
    browser.element('[id="calendar-monthly-pay-significant-changes-redundancies-answer-1"]').click()
    return this
  }

}

export default new CalendarMonthlyPaySignificantChangesRedundanciesPage()

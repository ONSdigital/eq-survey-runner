// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CalendarMonthlyPaySignificantChangesPaidEmployeesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('calendar-monthly-pay-significant-changes-paid-employees')
  }

  clickCalendarMonthlyPaySignificantChangesPaidEmployeesAnswerYes() {
    browser.element('[id="calendar-monthly-pay-significant-changes-paid-employees-answer-0"]').click()
    return this
  }

  clickCalendarMonthlyPaySignificantChangesPaidEmployeesAnswerNo() {
    browser.element('[id="calendar-monthly-pay-significant-changes-paid-employees-answer-1"]').click()
    return this
  }

}

export default new CalendarMonthlyPaySignificantChangesPaidEmployeesPage()

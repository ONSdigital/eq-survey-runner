// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CalendarMonthlyPaySignificantChangesTempEmployeesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('calendar-monthly-pay-significant-changes-temp-employees')
  }

  clickCalendarMonthlyPaySignificantChangesTempEmployeesAnswerMoreTemporaryStaff() {
    browser.element('[id="calendar-monthly-pay-significant-changes-temp-employees-answer-0"]').click()
    return this
  }

  clickCalendarMonthlyPaySignificantChangesTempEmployeesAnswerFewerTemporaryStaff() {
    browser.element('[id="calendar-monthly-pay-significant-changes-temp-employees-answer-1"]').click()
    return this
  }

  clickCalendarMonthlyPaySignificantChangesTempEmployeesAnswerNoSignificantChange() {
    browser.element('[id="calendar-monthly-pay-significant-changes-temp-employees-answer-2"]').click()
    return this
  }

}

export default new CalendarMonthlyPaySignificantChangesTempEmployeesPage()

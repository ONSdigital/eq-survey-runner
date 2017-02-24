// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class CalendarMonthlyPayPaidEmployeesPage extends QuestionPage {

  constructor() {
    super('calendar-monthly-pay-paid-employees')
  }

  setCalendarMonthlyPayPaidEmployeesAnswer(value) {
    browser.setValue('[name="calendar-monthly-pay-paid-employees-answer"]', value)
    return this
  }

  getCalendarMonthlyPayPaidEmployeesAnswer(value) {
    return browser.element('[name="calendar-monthly-pay-paid-employees-answer"]').getValue()
  }

}

export default new CalendarMonthlyPayPaidEmployeesPage()

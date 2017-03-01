// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class CalendarMonthlyPayGrossPayPage extends QuestionPage {

  constructor() {
    super('calendar-monthly-pay-gross-pay')
  }

  setCalendarMonthlyPayGrossPayAnswer(value) {
    browser.setValue('[name="calendar-monthly-pay-gross-pay-answer"]', value)
    return this
  }

  getCalendarMonthlyPayGrossPayAnswer(value) {
    return browser.element('[name="calendar-monthly-pay-gross-pay-answer"]').getValue()
  }

}

export default new CalendarMonthlyPayGrossPayPage()

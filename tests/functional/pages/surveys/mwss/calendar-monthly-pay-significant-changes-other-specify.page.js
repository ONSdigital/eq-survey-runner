// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class CalendarMonthlyPaySignificantChangesOtherSpecifyPage extends QuestionPage {

  constructor() {
    super('calendar-monthly-pay-significant-changes-other-specify')
  }

  setCalendarMonthlyPaySignificantChangesOtherSpecifyAnswer(value) {
    browser.setValue('[name="calendar-monthly-pay-significant-changes-other-specify-answer"]', value)
    return this
  }

  getCalendarMonthlyPaySignificantChangesOtherSpecifyAnswer(value) {
    return browser.element('[name="calendar-monthly-pay-significant-changes-other-specify-answer"]').getValue()
  }

}

export default new CalendarMonthlyPaySignificantChangesOtherSpecifyPage()

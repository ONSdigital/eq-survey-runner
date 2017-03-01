// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CalendarMonthlyPaySignificantChangesPayRatesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('calendar-monthly-pay-significant-changes-pay-rates')
  }

  clickCalendarMonthlyPaySignificantChangesPayRatesAnswerYes() {
    browser.element('[id="calendar-monthly-pay-significant-changes-pay-rates-answer-0"]').click()
    return this
  }

  clickCalendarMonthlyPaySignificantChangesPayRatesAnswerNo() {
    browser.element('[id="calendar-monthly-pay-significant-changes-pay-rates-answer-1"]').click()
    return this
  }

}

export default new CalendarMonthlyPaySignificantChangesPayRatesPage()

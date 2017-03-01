// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CalendarMonthlyPaySignificantChangesGrossPayPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('calendar-monthly-pay-significant-changes-gross-pay')
  }

  clickCalendarMonthlyPaySignificantChangesGrossPayAnswerYes() {
    browser.element('[id="calendar-monthly-pay-significant-changes-gross-pay-answer-0"]').click()
    return this
  }

  clickCalendarMonthlyPaySignificantChangesGrossPayAnswerNo() {
    browser.element('[id="calendar-monthly-pay-significant-changes-gross-pay-answer-1"]').click()
    return this
  }

}

export default new CalendarMonthlyPaySignificantChangesGrossPayPage()

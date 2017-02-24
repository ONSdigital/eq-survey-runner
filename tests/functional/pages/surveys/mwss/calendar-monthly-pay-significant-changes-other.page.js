// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class CalendarMonthlyPaySignificantChangesOtherPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('calendar-monthly-pay-significant-changes-other')
  }

  clickCalendarMonthlyPaySignificantChangesOtherAnswerYes() {
    browser.element('[id="calendar-monthly-pay-significant-changes-other-answer-0"]').click()
    return this
  }

  clickCalendarMonthlyPaySignificantChangesOtherAnswerNo() {
    browser.element('[id="calendar-monthly-pay-significant-changes-other-answer-1"]').click()
    return this
  }

}

export default new CalendarMonthlyPaySignificantChangesOtherPage()

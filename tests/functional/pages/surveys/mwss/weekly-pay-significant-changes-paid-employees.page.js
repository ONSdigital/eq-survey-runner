// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class WeeklyPaySignificantChangesPaidEmployeesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('weekly-pay-significant-changes-paid-employees')
  }

  clickWeeklyPaySignificantChangesPaidEmployeesAnswerYes() {
    browser.element('[id="weekly-pay-significant-changes-paid-employees-answer-0"]').click()
    return this
  }

  clickWeeklyPaySignificantChangesPaidEmployeesAnswerNo() {
    browser.element('[id="weekly-pay-significant-changes-paid-employees-answer-1"]').click()
    return this
  }

}

export default new WeeklyPaySignificantChangesPaidEmployeesPage()

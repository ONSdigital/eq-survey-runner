// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FiveWeeklyPaySignificantChangesPaidEmployeesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('five-weekly-pay-significant-changes-paid-employees')
  }

  clickFiveWeeklyPaySignificantChangesPaidEmployeesAnswerYes() {
    browser.element('[id="five-weekly-pay-significant-changes-paid-employees-answer-0"]').click()
    return this
  }

  clickFiveWeeklyPaySignificantChangesPaidEmployeesAnswerNo() {
    browser.element('[id="five-weekly-pay-significant-changes-paid-employees-answer-1"]').click()
    return this
  }

}

export default new FiveWeeklyPaySignificantChangesPaidEmployeesPage()

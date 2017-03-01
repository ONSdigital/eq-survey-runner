// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FourWeeklyPaySignificantChangesPaidEmployeesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('four-weekly-pay-significant-changes-paid-employees')
  }

  clickFourWeeklyPaySignificantChangesPaidEmployeesAnswerYes() {
    browser.element('[id="four-weekly-pay-significant-changes-paid-employees-answer-0"]').click()
    return this
  }

  clickFourWeeklyPaySignificantChangesPaidEmployeesAnswerNo() {
    browser.element('[id="four-weekly-pay-significant-changes-paid-employees-answer-1"]').click()
    return this
  }

}

export default new FourWeeklyPaySignificantChangesPaidEmployeesPage()

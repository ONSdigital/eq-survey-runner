// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FiveWeeklyPaySignificantChangesTempEmployeesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('five-weekly-pay-significant-changes-temp-employees')
  }

  clickFiveWeeklyPaySignificantChangesTempEmployeesAnswerMoreTemporaryStaff() {
    browser.element('[id="five-weekly-pay-significant-changes-temp-employees-answer-0"]').click()
    return this
  }

  clickFiveWeeklyPaySignificantChangesTempEmployeesAnswerFewerTemporaryStaff() {
    browser.element('[id="five-weekly-pay-significant-changes-temp-employees-answer-1"]').click()
    return this
  }

  clickFiveWeeklyPaySignificantChangesTempEmployeesAnswerNoSignificantChange() {
    browser.element('[id="five-weekly-pay-significant-changes-temp-employees-answer-2"]').click()
    return this
  }

}

export default new FiveWeeklyPaySignificantChangesTempEmployeesPage()

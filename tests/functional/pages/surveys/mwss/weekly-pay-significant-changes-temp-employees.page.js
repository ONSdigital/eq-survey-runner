// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class WeeklyPaySignificantChangesTempEmployeesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('weekly-pay-significant-changes-temp-employees')
  }

  clickWeeklyPaySignificantChangesTempEmployeesAnswerMoreTemporaryStaff() {
    browser.element('[id="weekly-pay-significant-changes-temp-employees-answer-0"]').click()
    return this
  }

  clickWeeklyPaySignificantChangesTempEmployeesAnswerFewerTemporaryStaff() {
    browser.element('[id="weekly-pay-significant-changes-temp-employees-answer-1"]').click()
    return this
  }

  clickWeeklyPaySignificantChangesTempEmployeesAnswerNoSignificantChange() {
    browser.element('[id="weekly-pay-significant-changes-temp-employees-answer-2"]').click()
    return this
  }

}

export default new WeeklyPaySignificantChangesTempEmployeesPage()

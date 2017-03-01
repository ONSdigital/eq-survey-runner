// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FourWeeklyPaySignificantChangesTempEmployeesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('four-weekly-pay-significant-changes-temp-employees')
  }

  clickFourWeeklyPaySignificantChangesTempEmployeesAnswerMoreTemporaryStaff() {
    browser.element('[id="four-weekly-pay-significant-changes-temp-employees-answer-0"]').click()
    return this
  }

  clickFourWeeklyPaySignificantChangesTempEmployeesAnswerFewerTemporaryStaff() {
    browser.element('[id="four-weekly-pay-significant-changes-temp-employees-answer-1"]').click()
    return this
  }

  clickFourWeeklyPaySignificantChangesTempEmployeesAnswerNoSignificantChange() {
    browser.element('[id="four-weekly-pay-significant-changes-temp-employees-answer-2"]').click()
    return this
  }

}

export default new FourWeeklyPaySignificantChangesTempEmployeesPage()

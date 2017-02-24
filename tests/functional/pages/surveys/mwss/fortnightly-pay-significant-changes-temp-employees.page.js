// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FortnightlyPaySignificantChangesTempEmployeesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('fortnightly-pay-significant-changes-temp-employees')
  }

  clickFortnightlyPaySignificantChangesTempEmployeesAnswerMoreTemporaryStaff() {
    browser.element('[id="fortnightly-pay-significant-changes-temp-employees-answer-0"]').click()
    return this
  }

  clickFortnightlyPaySignificantChangesTempEmployeesAnswerFewerTemporaryStaff() {
    browser.element('[id="fortnightly-pay-significant-changes-temp-employees-answer-1"]').click()
    return this
  }

  clickFortnightlyPaySignificantChangesTempEmployeesAnswerNoSignificantChange() {
    browser.element('[id="fortnightly-pay-significant-changes-temp-employees-answer-2"]').click()
    return this
  }

}

export default new FortnightlyPaySignificantChangesTempEmployeesPage()

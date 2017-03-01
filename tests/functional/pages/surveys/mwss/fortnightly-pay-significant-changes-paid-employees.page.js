// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FortnightlyPaySignificantChangesPaidEmployeesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('fortnightly-pay-significant-changes-paid-employees')
  }

  clickFortnightlyPaySignificantChangesPaidEmployeesAnswerYes() {
    browser.element('[id="fortnightly-pay-significant-changes-paid-employees-answer-0"]').click()
    return this
  }

  clickFortnightlyPaySignificantChangesPaidEmployeesAnswerNo() {
    browser.element('[id="fortnightly-pay-significant-changes-paid-employees-answer-1"]').click()
    return this
  }

}

export default new FortnightlyPaySignificantChangesPaidEmployeesPage()

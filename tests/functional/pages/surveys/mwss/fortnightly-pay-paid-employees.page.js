// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FortnightlyPayPaidEmployeesPage extends QuestionPage {

  constructor() {
    super('fortnightly-pay-paid-employees')
  }

  setFortnightlyPayPaidEmployeesAnswer(value) {
    browser.setValue('[name="fortnightly-pay-paid-employees-answer"]', value)
    return this
  }

  getFortnightlyPayPaidEmployeesAnswer(value) {
    return browser.element('[name="fortnightly-pay-paid-employees-answer"]').getValue()
  }

}

export default new FortnightlyPayPaidEmployeesPage()

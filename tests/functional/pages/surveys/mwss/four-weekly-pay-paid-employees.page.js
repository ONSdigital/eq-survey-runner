// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FourWeeklyPayPaidEmployeesPage extends QuestionPage {

  constructor() {
    super('four-weekly-pay-paid-employees')
  }

  setFourWeeklyPayPaidEmployeesAnswer(value) {
    browser.setValue('[name="four-weekly-pay-paid-employees-answer"]', value)
    return this
  }

  getFourWeeklyPayPaidEmployeesAnswer(value) {
    return browser.element('[name="four-weekly-pay-paid-employees-answer"]').getValue()
  }

}

export default new FourWeeklyPayPaidEmployeesPage()

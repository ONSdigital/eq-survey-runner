// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FiveWeeklyPayPaidEmployeesPage extends QuestionPage {

  constructor() {
    super('five-weekly-pay-paid-employees')
  }

  setFiveWeeklyPayPaidEmployeesAnswer(value) {
    browser.setValue('[name="five-weekly-pay-paid-employees-answer"]', value)
    return this
  }

  getFiveWeeklyPayPaidEmployeesAnswer(value) {
    return browser.element('[name="five-weekly-pay-paid-employees-answer"]').getValue()
  }

}

export default new FiveWeeklyPayPaidEmployeesPage()

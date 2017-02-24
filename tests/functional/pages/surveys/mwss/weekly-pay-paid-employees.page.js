// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class WeeklyPayPaidEmployeesPage extends QuestionPage {

  constructor() {
    super('weekly-pay-paid-employees')
  }

  setWeeklyPayPaidEmployeesAnswer(value) {
    browser.setValue('[name="weekly-pay-paid-employees-answer"]', value)
    return this
  }

  getWeeklyPayPaidEmployeesAnswer(value) {
    return browser.element('[name="weekly-pay-paid-employees-answer"]').getValue()
  }

}

export default new WeeklyPayPaidEmployeesPage()

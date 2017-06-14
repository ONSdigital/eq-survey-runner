// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class TotalEmployeesPage extends QuestionPage {
  constructor() {
    super('total-employees')
  }
  setTotalNumberEmployees(value) {
    browser.setValue('[name="total-number-employees"]', value)
    return this
  }
  getTotalNumberEmployees(value) {
    return browser.element('[name="total-number-employees"]').getValue()
  }
  getTotalNumberEmployeesLabel() {
    return browser.element('#label-total-number-employees')
  }
  getTotalNumberEmployeesElement() {
    return browser.element('[name="total-number-employees"]')
  }
}

export default new TotalEmployeesPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class Employees2016Page extends QuestionPage {

  constructor() {
    super('employees-2016')
  }

  setEmployees2016Answer(value) {
    browser.setValue('[name="employees-2016-answer"]', value)
    return this
  }

  getEmployees2016Answer(value) {
    return browser.element('[name="employees-2016-answer"]').getValue()
  }

}

export default new Employees2016Page()

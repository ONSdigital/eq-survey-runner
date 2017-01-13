// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class Employees2014Page extends QuestionPage {

  constructor() {
    super('employees-2014')
  }

  setEmployees2014Answer(value) {
    browser.setValue('[name="employees-2014-answer"]', value)
    return this
  }

  getEmployees2014Answer(value) {
    return browser.element('[name="employees-2014-answer"]').getValue()
  }

}

export default new Employees2014Page()

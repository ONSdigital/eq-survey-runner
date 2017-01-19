// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class EmployeesQualifications2016Page extends QuestionPage {

  constructor() {
    super('employees-qualifications-2016')
  }

  setEmployeesQualifications2016ScienceAnswer(value) {
    browser.setValue('[name="employees-qualifications-2016-science-answer"]', value)
    return this
  }

  getEmployeesQualifications2016ScienceAnswer(value) {
    return browser.element('[name="employees-qualifications-2016-science-answer"]').getValue()
  }

  setEmployeesQualificationsOther2016Answer(value) {
    browser.setValue('[name="employees-qualifications-other-2016-answer"]', value)
    return this
  }

  getEmployeesQualificationsOther2016Answer(value) {
    return browser.element('[name="employees-qualifications-other-2016-answer"]').getValue()
  }

}

export default new EmployeesQualifications2016Page()

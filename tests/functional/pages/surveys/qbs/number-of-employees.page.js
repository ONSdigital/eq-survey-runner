// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class NumberOfEmployeesPage extends QuestionPage {

  constructor() {
    super('number-of-employees')
  }

  setNumberOfEmployeesMaleMore30Hours(value) {
    browser.setValue('[name="number-of-employees-male-more-30-hours"]', value)
    return this
  }

  getNumberOfEmployeesMaleMore30Hours(value) {
    return browser.element('[name="number-of-employees-male-more-30-hours"]').getValue()
  }

  setNumberOfEmployeesMaleLess30Hours(value) {
    browser.setValue('[name="number-of-employees-male-less-30-hours"]', value)
    return this
  }

  getNumberOfEmployeesMaleLess30Hours(value) {
    return browser.element('[name="number-of-employees-male-less-30-hours"]').getValue()
  }

  setNumberOfEmployeesFemaleMore30Hours(value) {
    browser.setValue('[name="number-of-employees-female-more-30-hours"]', value)
    return this
  }

  getNumberOfEmployeesFemaleMore30Hours(value) {
    return browser.element('[name="number-of-employees-female-more-30-hours"]').getValue()
  }

  setNumberOfEmployeesFemaleLess30Hours(value) {
    browser.setValue('[name="number-of-employees-female-less-30-hours"]', value)
    return this
  }

  getNumberOfEmployeesFemaleLess30Hours(value) {
    return browser.element('[name="number-of-employees-female-less-30-hours"]').getValue()
  }

  setNumberOfEmployeesTotal(value) {
    browser.setValue('[name="number-of-employees-total"]', value)
    return this
  }

  getNumberOfEmployeesTotal(value) {
    return browser.element('[name="number-of-employees-total"]').getValue()
  }

}

export default new NumberOfEmployeesPage()

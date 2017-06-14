// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class EmployeesBreakdownPage extends QuestionPage {
  constructor() {
    super('employees-breakdown')
  }
  setNumberMaleEmployeesOver30Hours(value) {
    browser.setValue('[name="number-male-employees-over-30-hours"]', value)
    return this
  }
  getNumberMaleEmployeesOver30Hours(value) {
    return browser.element('[name="number-male-employees-over-30-hours"]').getValue()
  }
  getNumberMaleEmployeesOver30HoursLabel() {
    return browser.element('#label-number-male-employees-over-30-hours')
  }
  getNumberMaleEmployeesOver30HoursElement() {
    return browser.element('[name="number-male-employees-over-30-hours"]')
  }
  setNumberMaleEmployeesUnder30Hours(value) {
    browser.setValue('[name="number-male-employees-under-30-hours"]', value)
    return this
  }
  getNumberMaleEmployeesUnder30Hours(value) {
    return browser.element('[name="number-male-employees-under-30-hours"]').getValue()
  }
  getNumberMaleEmployeesUnder30HoursLabel() {
    return browser.element('#label-number-male-employees-under-30-hours')
  }
  getNumberMaleEmployeesUnder30HoursElement() {
    return browser.element('[name="number-male-employees-under-30-hours"]')
  }
  setNumberFemaleEmployeesOver30Hours(value) {
    browser.setValue('[name="number-female-employees-over-30-hours"]', value)
    return this
  }
  getNumberFemaleEmployeesOver30Hours(value) {
    return browser.element('[name="number-female-employees-over-30-hours"]').getValue()
  }
  getNumberFemaleEmployeesOver30HoursLabel() {
    return browser.element('#label-number-female-employees-over-30-hours')
  }
  getNumberFemaleEmployeesOver30HoursElement() {
    return browser.element('[name="number-female-employees-over-30-hours"]')
  }
  setNumberFemaleEmployeesUnder30Hours(value) {
    browser.setValue('[name="number-female-employees-under-30-hours"]', value)
    return this
  }
  getNumberFemaleEmployeesUnder30Hours(value) {
    return browser.element('[name="number-female-employees-under-30-hours"]').getValue()
  }
  getNumberFemaleEmployeesUnder30HoursLabel() {
    return browser.element('#label-number-female-employees-under-30-hours')
  }
  getNumberFemaleEmployeesUnder30HoursElement() {
    return browser.element('[name="number-female-employees-under-30-hours"]')
  }
}

export default new EmployeesBreakdownPage()

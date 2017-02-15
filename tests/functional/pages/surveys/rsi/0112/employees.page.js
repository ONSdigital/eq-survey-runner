import QuestionPage from '../../question.page'

class EmployeesPage extends QuestionPage {

  setMaleEmployeesOver30Hours(employees) {
    browser.setValue('[name="male-employees-over-30-hours"]', employees)
    return this
  }

  setTotalEmployees(employees) {
    browser.setValue('[name="total-number-employees"]', employees)
    return this
  }

}

export default new EmployeesPage()

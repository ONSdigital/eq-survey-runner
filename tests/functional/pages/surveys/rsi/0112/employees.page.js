import QuestionPage from '../../question.page'

class EmployeesPage extends QuestionPage {

  setEmployees(employees) {
    browser.setValue('[name="total-number-employees"]', employees)
    return this
  }

}

export default new EmployeesPage()

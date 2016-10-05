import QuestionPage from '../../question.page'

class EmployeesPage extends QuestionPage {

  setEmployees(employees) {
    browser.setValue('[name="c6881970-98ff-4005-af4a-60bfd9b6179f"]', employees)
    return this
  }

}

module.exports = new EmployeesPage()

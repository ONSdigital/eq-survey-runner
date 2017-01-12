import QuestionPage from '../../question.page'

class ChangesInEmployeesPage extends QuestionPage {

  setChangesInEmployeesPage(reason) {
    browser.setValue('[name="changes-in-employees-answer"]', reason)
    return this
  }

}

export default new ChangesInEmployeesPage()

import QuestionPage from '../../question.page'

class ChangesInEmployeesPage extends QuestionPage {

  setChangesInEmployeesPage(reason) {
    browser.setValue('[name="414699da-1667-44fd-8e98-7606966884db"]', reason)
    return this
  }

}

module.exports = new ChangesInEmployeesPage()

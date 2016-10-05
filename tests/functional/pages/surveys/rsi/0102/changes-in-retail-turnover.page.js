import QuestionPage from '../../question.page'

class ChangesInRetailTurnoverPage extends QuestionPage {

  setChangesInRetailTurnover(changes) {
    browser.setValue('[name="568e2c81-b11d-4682-bd89-f170481c9a48"]', changes)
    return this
  }

}

export default new ChangesInRetailTurnoverPage()

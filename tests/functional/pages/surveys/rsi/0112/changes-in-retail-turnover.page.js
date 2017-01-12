import QuestionPage from '../../question.page'

class ChangesInRetailTurnoverPage extends QuestionPage {

  setChangesInRetailTurnover(changes) {
    browser.setValue('[name="changes-in-retail-turnover-answer"]', changes)
    return this
  }

}

export default new ChangesInRetailTurnoverPage()

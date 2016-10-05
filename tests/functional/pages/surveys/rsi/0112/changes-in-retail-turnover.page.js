import QuestionPage from '../../question.page'

class ChangesInRetailTurnoverPage extends QuestionPage {

  setChangesInRetailTurnover(changes) {
    browser.setValue('[name="287e8c33-9d52-4589-9c1c-3db11d0eec20"]', changes)
    return this
  }

}

module.exports = new ChangesInRetailTurnoverPage()

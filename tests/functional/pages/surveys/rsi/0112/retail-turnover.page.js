import QuestionPage from '../../question.page'

class RetailTurnoverPage extends QuestionPage {

  setRetailTurnover(turnover) {
    browser.setValue('[name="fe88fa9a-3c49-4fbc-9408-a91c0a1cc6d5"]', turnover)
    return this
  }

}

module.exports = new RetailTurnoverPage()

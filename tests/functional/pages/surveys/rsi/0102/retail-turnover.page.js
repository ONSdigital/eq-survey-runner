import QuestionPage from '../../question.page'

class RetailTurnoverPage extends QuestionPage {

  setRetailTurnover(turnover) {
    browser.setValue('[name="ea08f977-33a8-4933-ad7b-c497997107cf"]', turnover)
    return this
  }

}

module.exports = new RetailTurnoverPage()
